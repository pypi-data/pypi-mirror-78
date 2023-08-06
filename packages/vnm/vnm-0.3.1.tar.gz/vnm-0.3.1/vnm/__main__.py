import json
import collections
import argparse
import tempfile
import sys
import logging
import os
import shutil
import re
import enum
import string
import types
from typing import Tuple, List, Any, Dict
from ruamel.yaml import YAML

from vnm.consts import PROG, NAME, VAR_PREFIX, DESC

log = logging.getLogger(__name__)
if sys.version_info < (3, 6):
    print(f'CRITICAL: `{PROG}` MUST be run with Python 3.6 or higher. You are running v'+ ('.'.join(sys.version)))
    sys.exit(1)

import urllib.request
import urllib.parse
from typing import Optional, List
from subprocess import check_call, check_output, call, CalledProcessError, Popen, PIPE
from wheel.wheelfile import WheelFile

from vnm.repos import *
from vnm.constraint import Constraint
from vnm.package import Package
from vnm.venv import activate, deactivate, setEnv, defined, unsetEnv

VENVDIR = os.path.abspath('.venv')

yaml = YAML(typ='rt')

def require_pipjson():
    if not os.path.isfile('pip.json') and not os.path.isfile('vnm.yml'):
        print('CRITICAL: I can\'t find pip.json nor vnm.yml!')
        sys.exit(1)

def require_venv():
    if 'VIRTUAL_ENV' not in os.environ:
        print(f'CRITICAL: This command must be run from a venv virtual environment. Did you run `{PROG} activate`? (VIRTUAL_ENV not set.)')
        sys.exit(1)

def getPython():
    pyexe = 'python.exe' if os.name == 'nt' else 'python'
    subdir = 'Scripts' if os.name == 'nt' else 'bin'
    return os.path.abspath(os.path.join(VENVDIR, subdir, pyexe))

def update_pip(args):
    xml = ''
    with urllib.request.urlopen('https://pypi.org/rss/project/pip/releases.xml') as u:
        #<title>20.2b1</title>
        xml = u.read().decode('utf-8')
    #print(xml)
    m = re.search(r'<title>([0-9\.]+)</title>', xml)
    assert m is not None
    upstream_version = m[1]

    o = check_output([getPython(), '-m', 'pip', '--version']).decode('utf-8')
    m = re.search(r'pip ([^ ]+) from (.*)', o)
    assert m is not None
    pip_version = m[1]

    print('Installed pip version: '+pip_version)
    print('Newest pip version...: '+upstream_version)
    if upstream_version!=pip_version:
        print('Updating pip...')
        check_call([getPython(), '-m', 'pip', 'install', '-U', 'pip'])

class EPipOperation(enum.IntEnum):
    INSTALL = enum.auto()
    REINSTALL = enum.auto()
    UPGRADE = enum.auto()

class ConfigState(object):
    PIPJSON_VERSION = 1
    VNMYML_VERSION = 3
    STATE_FILENAME = 'vnm.state'
    STATE_VERSION = '202007131859'
    def __init__(self, args: Optional[argparse.Namespace] = None):
        self.as_json: bool = False
        self.dev_mode: bool = False
        self.packages: Dict[str, Package] = {}
        self.dev_packages: Dict[str, Package] = {}

        self.yaml_upgrades: Dict[int, Callable] = {}
        self.state_upgrades: Dict[Any, Callable] = {}

        def addVnmYamlUpgrade(forVersion: int):
            def _wrap(process: callable) -> callable:
                self.yaml_upgrades[forVersion] = process
                return process
            return _wrap

        @addVnmYamlUpgrade(1)
        def vnmYmlv2(docs):
            docs[0]={'VERSION': 2}
            return docs

        @addVnmYamlUpgrade(2)
        def vnmYmlv3(docs):
            newdoc = {
                'version': 3,
                'packages': docs[1]['packages']
            }
            if 'dev-packages' in docs[1]:
                newdoc['dev-packages'] = docs[1]['dev-packages']
            return [newdoc]

        def addVnmStateUpgrade(forVersion: Any):
            def _wrap(process: callable) -> callable:
                self.state_upgrades[forVersion] = process
                return callable
            return _wrap

        @addVnmStateUpgrade('202006122014')
        def vnmState_2020_07_13_1859(docs):
            return ['202007131859', docs[2]]

    def getYamlVersion(self, docs) -> int:
        # 202006122014
        #if isinstance(docs, )
        if isinstance(docs, list):
            if isinstance(docs[0], int):
                return docs[0]
            elif isinstance(docs[0], dict):
                if 'VERSION' in docs[0]:
                    return docs[0]['VERSION']
                if 'version' in docs[0]:
                    return docs[0]['version']
                return self.PIPJSON_VERSION
            else:
                raise ArgumentError('docs', 'Invalid type {0} for vnm.yml:docs[0]'.format(type(docs[0])))
        elif isinstance(docs, dict):
            return docs.get('version', self.VNMYML_VERSION)

    def getStateVersion(self, docs) -> str:
        if isinstance(docs, list):
            if isinstance(docs[0], int):
                return str(docs[0])
            elif isinstance(docs[0], str):
                return docs[0]
            raise ArgumentError('docs', 'Invalid type {0} for vnm.state:docs[0]'.format(type(docs[0])))
        else:
            raise ArgumentError('docs', 'Invalid type {0} for vnm.state:docs'.format(type(docs)))

    def load(self) -> None:
        self.as_json = False
        data = {}
        statedata = {}
        if os.path.isfile('vnm.yml'):
            with open('vnm.yml', 'r') as f:
                docs = yaml.load_all(f)
                if isinstance(docs, types.GeneratorType):
                    docs = list(docs)
                version = self.getYamlVersion(docs)
                while version in self.yaml_upgrades:
                    print(f'WARNING: Updating vnm.yml to version {version+1}...')
                    docs = self.yaml_upgrades[version](docs)
                    version = self.getYamlVersion(docs)
                #print(repr(docs))
                data = docs[0]
        elif os.path.isfile('pip.json'):
            print('WARNING: pip.json is deprecated.')
            self.as_json=True
            with open('pip.json', 'r') as f:
                data = json.load(f)

        if os.path.isfile('vnm.state'):
            with open('vnm.state', 'r') as f:
                docs = list(yaml.load_all(f))
                version = self.getStateVersion(docs)
                while version in self.state_upgrades:
                    docs = self.state_upgrades[version](docs)
                    version = self.getStateVersion(docs)
                    print(f'WARNING: Updated vnm.state to version {version}...')
                statedata = docs[1]
                self.dev_mode = statedata.get('dev-mode', False)

        pkgdata = data.get('packages', {})
        for k, v in pkgdata.items():
            pkg = Package()
            pkg.id = k
            pkg.deserialize(v)
            self.packages[k] = pkg

        pkgdata = data.get('dev-packages', {})
        for k, v in pkgdata.items():
            pkg = Package()
            pkg.id = k
            pkg.deserialize(v)
            self.dev_packages[k] = pkg

    def get_packages(self) -> Dict[str, Package]:
        o = self.packages.copy()
        if self.dev_mode:
            o.update(self.dev_packages)
        return o

    def get_all_packages(self) -> Dict[str, Package]:
        return {**self.packages, **self.dev_packages}

    def _serialize_pkg_dict(self, d):
        o = collections.OrderedDict()
        for k in sorted(d.keys()):
            o[k]=d[k].serialize()
        return dict(o)
    def saveVNM(self, dry_run: bool=False) -> None:
        if self.as_json:
            data = {
                'version': self.PIPJSON_VERSION,
            }
            if len(self.packages) > 0:
                data['packages'] = self._serialize_pkg_dict(self.packages)
            if len(self.dev_packages) > 0:
                data['dev-packages'] = self._serialize_pkg_dict(self.dev_packages)
            with open('pip.new.json' if dry_run else 'pip.json', 'w') as f:
                json.dump(data, f, indent=2)
        else:
            data = {'version': self.VNMYML_VERSION}
            if len(self.packages) > 0:
                data['packages'] = self._serialize_pkg_dict(self.packages)
            if len(self.dev_packages) > 0:
                data['dev-packages'] = self._serialize_pkg_dict(self.dev_packages)
            with open('vnm.new.yml' if dry_run else 'vnm.yml', 'w') as f:
                f.write('# Generated by vnm.\n')
                yaml.dump(data, f)

    def saveState(self, dry_run: bool=False) -> None:
        data={}
        if self.dev_mode:
            data['dev-mode']=True
        # Mostly for debugging purposes.
        if self.as_json:
            data['as-json']=True
        with open(self.STATE_FILENAME + ('.new' if dry_run else ''), 'w') as f:
            f.write(f'# vnm state file version {self.STATE_VERSION}\n')
            f.write('# @GENERATED automatically by vnm.\n')
            f.write('# Do NOT edit this file, nor commit it to your VCS.\n')
            f.write('###################################################\n')
            f.write(f'{self.STATE_VERSION!r}\n')
            f.write(f'---\n')
            yaml.dump(data, f)

def install_venv(args: argparse.Namespace, cfg: ConfigState, operation=EPipOperation.INSTALL) -> List[Package]:
    pipargs = []
    verb = 'Installing'
    if operation == EPipOperation.REINSTALL:
        pipargs += ['-I']
        verb = 'Reinstalling'
    elif operation == EPipOperation.UPGRADE:
        pipargs += ['-U']
        verb = 'Upgrading'

    if len(cfg.packages) == 0 and len(cfg.dev_packages) == 0:
        return
    print('Writing temporary requirements file...')
    workdir = os.getcwd()
    tempfilename = ''
    all_packages: List[Package] = []
    try:
        if os.path.isfile('BROKEN-requirements.txt'):
            os.remove('BROKEN-requirements.txt')
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as f:
            tempfilename = f.name
            for pid, pkg in cfg.get_packages().items():
                f.write(pkg.toRequirement()+'\n')
        print(f'{verb} packages from {tempfilename}...')
        check_call([getPython(), '-m', 'pip', 'install']+pipargs+['-r', tempfilename])
        '''
        with open(os.path.join(workdir, 'requirements.txt'), 'w') as f:
            for pid, pkg in cfg.packages.items():
                f.write(pkg.toRequirement()+'\n')
                all_packages += [pkg]
        with open(os.path.join(workdir, 'requirements-dev.txt'), 'w') as f:
            for pid, pkg in cfg.dev_packages.items():
                f.write(pkg.toRequirement()+'\n')
                all_packages += [pkg]
        '''
    except CalledProcessError as cpe:
        if os.path.isfile(tempfilename):
            shutil.copy(tempfilename, 'BROKEN-requirements.txt')
    finally:
        if os.path.isfile(tempfilename):
            os.remove(tempfilename)
    return all_packages

def update_requirements(cfg, args, all_packages):
    p = Popen([getPython(), '-m', 'pip', 'freeze'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    suffix = '-dev' if cfg.dev_mode else ''
    if p.returncode == 0:
        all_package_names = []
        pkgs = {}
        for pkg in cfg.get_all_packages().values():
            all_package_names += [pkg.id.lower()]
            pkgs[pkg.id.lower()] = pkg
        for line in stdout.splitlines():
            #print(line)
            #oline = line
            line = line.strip()
            p = Package(line.decode('utf-8'))
            pkg = None
            if p.id.lower() in all_package_names:
                pkg = pkgs[p.id.lower()]
            #else:
            #    f.write(f'#{p.toRequirement()}\n')
            if pkg is not None:
                if len(pkg.constraints) == 0:
                    pkg.constraints = p.constraints
                if isinstance(pkg.repo, GitRepo) and isinstance(p.repo, GitRepo) and pkg.repo.refid != p.repo.refid:
                    pkg.repo = p.repo
            #print(line, pkg.id if pkg is not None else None, json.dumps(pkg.serialize()) if pkg is not None else None)

        all_release_pkgs = [k.lower() for k in cfg.packages.keys()]
        all_pkgs = all_release_pkgs+[k.lower() for k in cfg.dev_packages.keys()]
        with open(f'requirements.new.txt' if args.dry_run else f'requirements.txt', 'w') as f:
            for pkg in pkgs.values():
                if pkg.id.lower() in all_release_pkgs:
                    f.write(f'{pkg.toRequirement()}\n')
        if cfg.dev_mode:
            with open(f'requirements-dev.new.txt' if args.dry_run else f'requirements-dev.txt', 'w') as f:
                for pkg in pkgs.values():
                    if pkg.id.lower() in all_pkgs:
                        f.write(f'{pkg.toRequirement()}\n')
def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    argp = argparse.ArgumentParser(prog=PROG, description=DESC)
    argp.add_argument('--dry-run', action='store_true', default=False, help='Don\'t actually do anything.')
    subp = argp.add_subparsers()

    p_upgrade = subp.add_parser('upgrade', aliases=['u'], help='Upgrade all packages defined in vnm.yml to their latest available versions.')
    p_upgrade.set_defaults(cmd=_cmd_upgrade)

    p_upgrade_config = subp.add_parser('upgrade-config', help='Upgrade from pip.json to vnm.yml.')
    p_upgrade_config.set_defaults(cmd=_cmd_upgrade_config)

    p_install = subp.add_parser('install', aliases=['i'], help='Install all packages defined in vnm.yml')
    p_install.add_argument('--dev', '-d', action='store_true', default=False, help='Install in development mode. (Adds dev-packages.)')
    p_install.set_defaults(cmd=_cmd_install)

    p_init = subp.add_parser('init', help='Set up an initial .venv and vnm.yml.')
    p_init.add_argument('--clobber', action='store_true', default=False, help="Forcefully reinstall .venv and vnm.yml.")
    p_init.set_defaults(cmd=_cmd_init)

    p_add = subp.add_parser('add', help='Add a dependency to vnm.yml')
    p_add.add_argument('package', nargs='+', help="A package name or pip URI.")
    p_add.add_argument('--dev', '-d', action='store_true', default=False, help='All packages provided are development packages.')
    p_add.add_argument('--editable', '-e', nargs='+', type=str, help="A package name or pip URI (installed with -e).")
    p_add.add_argument('--force-reinstall', action='store_true', default=False, help="Forcefully reinstall all packages.")
    p_add.set_defaults(cmd=_cmd_add)

    p_remove = subp.add_parser('remove', aliases=['rm'], help='Remove package(s)')
    p_remove.add_argument('package', nargs='+', help="Package names.")
    p_remove.add_argument('--dev', '-d', action='store_true', default=False, help='All packages provided are development packages.')
    p_remove.set_defaults(cmd=_cmd_remove)

    p_activate = subp.add_parser('activate', aliases=['a'], help='Activate virtual environment.')
    p_activate.set_defaults(cmd=_cmd_activate)

    p_freeze = subp.add_parser('freeze', aliases=['f'], help='Freeze package version.')
    p_freeze.add_argument('packages', nargs='*', help="Package names.")
    p_freeze.set_defaults(cmd=_cmd_freeze)

    p_thaw = subp.add_parser('thaw', aliases=['t'], help='Thaw package version.')
    p_thaw.add_argument('packages', nargs='*', help="Package names.")
    p_thaw.add_argument('--constraints', action='store_true', default=False, help="Also wipe all version constraints.")
    p_thaw.set_defaults(cmd=_cmd_thaw)

    p_run = subp.add_parser('run', aliases=['r'], help='Run a python script in the virtual environment.')
    p_run.add_argument('filename', help='The python script or command to run')
    p_run.add_argument('args', nargs=argparse.REMAINDER, help='The python script to run')

    p_dumpenv = subp.add_parser('dump-env', help='Dump current environment variables.')
    p_dumpenv.add_argument('--format', choices=['text', 'json'], default='text', help='Format to output in')
    p_dumpenv.set_defaults(cmd=_cmd_dump_env)

    args = argp.parse_args()

    if getattr(args, 'cmd', None) is None:
        argp.print_usage()
    else:
        args.cmd(args)

def _sort_dict(d: dict) -> dict:
    nd = collections.OrderedDict()
    for k in sorted(d.keys()):
        nd[k]=d[k]
    return dict(nd)

def _cmd_add(args) -> None:
    require_venv()

    cfg = ConfigState()
    cfg.load()

    newpkgs = []
    all_packages = []
    for packagedef in args.package:
        pkg = Package(packagedef)
        print(f'Adding {pkg}...')
        if pkg.id not in (None, '') and pkg.id in cfg.packages:
            print(f'WARNING: Package {pkg.id!r} exists in {cfg.get_filename()}.')
        if args.dev:
            cfg.dev_packages[pkg.id] = pkg
        else:
            cfg.packages[pkg.id] = pkg
        if (cfg.dev_mode and args.dev) or (not cfg.dev_mode and not args.dev):
            newpkgs += pkg.toPipArgs()

    cfg.saveState(args.dry_run)
    cfg.saveVNM(args.dry_run)

    # Same as _cmd_install().
    activate(VENVDIR)
    update_pip(args)
    all_packages = install_venv(args, cfg)
    deactivate(VENVDIR)

    update_requirements(cfg, args, all_packages)

def _cmd_freeze(args) -> None:
    require_venv()

    cfg = ConfigState()
    cfg.load()

    pkgs_to_freeze = []
    for packagedef in args.packages:
        pkg = Package(packagedef)
        if pkg.id not in (None, '') and pkg.id not in cfg.get_all_packages():
            print(f'WARNING: Package {pkg.id!r} not specified in vnm.yml/pip.json.')
        pkgs_to_freeze += [pkg.id]


    p = Popen([getPython(), '-m', 'pip', 'freeze'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    suffix = '-dev' if cfg.dev_mode else ''
    if p.returncode == 0:
        all_package_names = []
        pkgs = {}
        for pkg in cfg.get_all_packages().values():
            all_package_names += [pkg.id.lower()]
            pkgs[pkg.id.lower()] = pkg
        for line in stdout.splitlines():
            #print(line)
            #oline = line
            line = line.strip()
            p = Package(line.decode('utf-8'))
            pkg = None
            if p.id.lower() in all_package_names:
                pkg = pkgs[p.id.lower()]

            if pkg is None:
                print(f'{p.id} not in package list.')
                continue

            if len(pkgs_to_freeze) == 0 or pkg.id in pkgs_to_freeze:
                if len(p.constraints) == 0:
                    print(f'WARNING: Package {p.id} has no version info')
                    continue
                if len(p.constraints) > 1:
                    pc = ', '.join([x.toRequirement() for x in p.constraints])
                    print(f'WARNING: Package {p.id} has a bunch of constraints. ({pc})')
                    continue
                pkg.freezeAt(p.constraints[0])
                if isinstance(pkg.repo, GitRepo) and isinstance(p.repo, GitRepo) and pkg.repo.refid != p.repo.refid:
                    pkg.repo = p.repo

                if pkg.id in cfg.dev_packages.keys():
                    print(f'Freezing dev package {pkg.id!r}')
                    cfg.dev_packages[pkg.id].freezeAt(p.constraints[0])
                if pkg.id in cfg.packages.keys():
                    print(f'Freezing package {pkg.id!r}')
                    cfg.packages[pkg.id].freezeAt(p.constraints[0])


    cfg.saveState()
    cfg.saveVNM()

    # Same as _cmd_install().
    activate(VENVDIR)
    update_pip(args)
    all_packages = install_venv(args, cfg)
    deactivate(VENVDIR)

    update_requirements(cfg, args, all_packages)

def _cmd_thaw(args) -> None:
    require_venv()

    cfg = ConfigState()
    cfg.load()

    pkgs_to_thaw = []
    for packagedef in args.packages:
        pkg = Package(packagedef)
        if pkg.id not in (None, '') and pkg.id not in cfg.get_all_packages():
            print(f'WARNING: Package {pkg.id!r} not specified in vnm.yml/pip.json.')
        pkgs_to_thaw += [pkg.id.lower()]

    for pkg in cfg.dev_packages.values():
        if len(args.packages) == 0 or pkg.id.lower() in pkgs_to_thaw:
            print(f'Thawing dev package {pkg.id!r}')
            pkg.thaw()
            if args.constraints:
                pkg.constraints = []
    for pkg in cfg.packages.values():
        if len(args.packages) == 0 or pkg.id.lower() in pkgs_to_thaw:
            print(f'Thawing package {pkg.id!r}')
            pkg.thaw()
            if args.constraints:
                pkg.constraints = []

    cfg.saveState()
    cfg.saveVNM()

    # Same as _cmd_install().
    activate(VENVDIR)
    update_pip(args)
    all_packages = install_venv(args, cfg)
    deactivate(VENVDIR)

    update_requirements(cfg, args, all_packages)

def _cmd_remove(args) -> None:
    require_venv()

    cfg = ConfigState()
    cfg.load()

    rmpkgs = []
    all_packages = []
    for packagedef in args.package:
        pkg = Package(packagedef)
        print(f'Removing {pkg}...')
        if pkg.id not in (None, '') and pkg.id not in cfg.get_all_packages():
            print(f'  WARNING: Package {pkg.id} not specified in vnm.yml/pip.json.')
        if pkg.id in cfg.packages:
            del cfg.packages[pkg.id]
        if pkg.id in cfg.dev_packages:
            del cfg.dev_packages[pkg.id]
        rmpkgs += [pkg.id]

    cfg.saveState(args.dry_run)
    cfg.saveVNM(args.dry_run)

    # Same as _cmd_install().
    activate(VENVDIR)
    update_pip(args)
    call([getPython(), '-m', 'pip', 'uninstall', '-y']+rmpkgs)
    deactivate(VENVDIR)

    update_requirements(cfg, args, all_packages)

def _cmd_upgrade(args):
    require_venv()
    require_pipjson()

    cfg = ConfigState()
    cfg.load()

    activate(VENVDIR)
    update_pip(args)
    all_packages = install_venv(args, cfg, operation=EPipOperation.UPGRADE)
    deactivate(VENVDIR)

    update_requirements(cfg, args, all_packages)

def _cmd_upgrade_config(args):
    require_pipjson()

    cfg = ConfigState()

    if os.path.isfile('pip.json'):
        print('WARNING: Upgrading pip.json to vnm.yml...')
        if not os.path.isfile('pip.json.bak'):
            print('Backing up pip.json to pip.json.bak...')
            shutil.copy('pip.json', 'pip.json.bak')
        else:
            print("pip.json.bak exists, skipping backup.")
        print('Reading...')
        cfg.load()
        if not args.dry_run:
            print('Removing pip.json...')
            os.remove('pip.json')
    elif os.path.isfile('vnm.yml'):
        print('WARNING: Upgrading vnm.yml...')
        if not os.path.isfile('vnm.yml.bak'):
            print('Backing up vnm.yml to vnm.yml.bak...')
            shutil.copy('vnm.yml', 'vnm.yml.bak')
        else:
            print("vnm.yml.bak exists, skipping backup.")
        print('Reading...')
        cfg.load()
    else:
        print('CRITICAL: Neither vnm.yml nor pip.json are present.  Exiting.')
        sys.exit(1)
    print('Writing vnm.yml...')
    cfg.as_json = False
    cfg.saveState(args.dry_run)
    cfg.saveVNM(args.dry_run)

def _cmd_install(args):
    if not os.path.isfile('vnm.yml'):
        if not os.path.isfile('pip.json'):
            print(f'CRITICAL: vnm.yml is missing.  This project is not set up for {NAME}.')
            return
        print('WARNING: pip.json is deprecated.')
    if not os.path.isfile(getPython()):
        print('WARNING: Virtual environment not installed. Initializing...')
        clear_cmd = [sys.executable, '-m', 'venv']
        if os.path.isdir('.venv'):
            clear_cmd += ['--clear']
        clear_cmd += ['.venv']
        clear_cmd = ' '.join(clear_cmd)
        print(f'Running {clear_cmd}...')
        check_call(clear_cmd)
    #require_venv()
    require_pipjson()

    cfg = ConfigState()
    cfg.load()
    cfg.dev_mode = args.dev
    cfg.saveState()

    activate(VENVDIR)
    update_pip(args)
    all_packages = install_venv(args, cfg)
    deactivate(VENVDIR)

    update_requirements(cfg, args, all_packages)

def _cmd_init(args):
    if (os.path.isfile('pip.json') or os.path.isfile('vnm.yml')) and not args.clobber:
        print('CRITICAL: pip.json or vnm.yml exists, aborting.  If you REALLY want to re-init the project, please set --clobber.')
        return

    print('Cleaning up prior install...')
    if os.path.isfile('pip.json'):
        print('rm pip.json')
        os.remove('pip.json')
    if os.path.isfile('vnm.yml'):
        print('rm vnm.yml')
        os.remove('vnm.yml')
    clear_cmd = [sys.executable, '-m', 'venv', '--clear', '.venv']
    clear_cmd_str = ' '.join(clear_cmd)
    print(f'Running {clear_cmd_str}...')
    check_call(clear_cmd)

    print('Writing vnm.yml...')
    cfg = ConfigState()
    cfg.saveVNM()
    cfg.saveState()

    #update_pip(args)
    print( '********************************************************************')
    print(f'.venv for {NAME} installed!')
    print( 'Next steps:')
    print(f'  1. Run `{PROG} activate` to activate the virtual environment.')
    print(f'  2. Add packages with `{PROG} add <package>` OR edit .')
    print( '  3. Add vnm.yml and requirements.txt to your VCS (if applicable).')
    print( '********************************************************************')

def _cmd_dump_env(args):
    data = {
        'os.environ':os.environ,
        'sys.path':sys.path,
    }
    if args.format == 'json':
        print(json.dumps(data))
    else:
        print('os.environ:')
        for key, value in os.environ.items():
            print(f'  {key}: {value!r}')
        print('sys.path:')
        for value in sys.path:
            print(f'  - {value}')

def _cmd_activate(args):
    if not os.path.isfile(getPython()):
        print(f'CRITICAL: Virtual environment not installed. Did you run `{PROG} init`?', PROG)
        return
    if f'_{VAR_PREFIX}_ACTIVE' in os.environ:
        log.critical(f'You are already in a {NAME} virtual environment, you doofus.')
        sys.exit(1)
        return

    if os.name == 'nt':
        _cmd_activate_nt(args)
    else:
        _cmd_activate_bash(args)

def _cmd_activate_nt(args):
    activate(VENVDIR)
    oldprompt = os.environ['PROMPT']
    os.environ['PROMPT'] = f'[{NAME}] {oldprompt}'
    print('='*60)
    print('Great, all done.')
    print('You are now in a child cmd.exe shell with the virtual environment set up for you.')
    print('You can deactivate the environment at any time by using the `exit` command.')
    print('='*60)
    def hide_script(a):
        if os.path.isfile(a):
            if os.path.isfile(a+'bak'):
                os.remove(a+'.bak')
            shutil.move(a, a+'.bak')
    def unhide_script(a):
        if os.path.isfile(a):
            os.remove(a)
        shutil.move(a+'.bak', a)
    hide_script(os.path.join(VENVDIR, 'Scripts', 'deactivate.bat'))
    code = -1
    try:
        code = call(['cmd.exe'], shell=True)
    finally:
        print(f'{PROG}: cmd.exe exited with code {code}')
        unhide_script(os.path.join(VENVDIR, 'Scripts', 'deactivate.bat'))
        deactivate(VENVDIR)
        os.environ['PROMPT'] = oldprompt

def _cmd_activate_bash(args):
    filename = ''
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        filename = f.name

        def writeNDebug(line):
            log.debug('Writing %r...', line)
            f.write(line)

        writeNDebug('echo "Activating..."\n')

        writeNDebug(f'. ~/.bashrc\n')
        writeNDebug(f'. {VENVDIR}/bin/activate\n')

        # Don't want users escaping by the normal means
        writeNDebug(f'unset -f deactivate\n')
        writeNDebug('alias deactivate=exit\n')
        writeNDebug(f'export _{VAR_PREFIX}_ACTIVE=1\n')
        writeNDebug(f'export _{VAR_PREFIX}_PROCESS={os.getpid()}\n')
        writeNDebug(f'PS1="[{NAME}] ${{PS1}}"\n')

        bar = '='*60
        writeNDebug(f'echo "{bar}"\n')
        writeNDebug('echo "Great, all done."\n')
        writeNDebug('echo "You are now in a child bash shell with the virtual environment set up for you."\n')
        writeNDebug('echo "You can deactivate the environment at any time by using the \\`exit\\` command."\n')
        writeNDebug(f'echo "{bar}"\n')
    code = call(['/bin/bash', '--init-file', filename])
    print(f'{PROG}: bash exited with code {code}')
    os.remove(filename)


#def _cmd_deactivate(args):
#    from vnm.venv import deactivate
#    deactivate('.venv')

def _cmd_run(args):
    from vnm.venv import runFrom
    runFrom('.venv', args.filename, args.args)

if __name__ == '__main__':
    main()
