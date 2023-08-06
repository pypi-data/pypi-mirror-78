import re
import os
from typing import Optional, List
from vnm.repos import *
from vnm.constraint import Constraint
class Package(object):
    REGEX_CONSTRAINTS=re.compile(r'(?P<equality>(==|>=|<=|>|<))(?P<version>[0-9\.]+)')
    REGEX_PACKAGENAME=re.compile(r'^([a-zA-Z0-9_\-\.]+)')

    @classmethod
    def FromJSON(cls, data: dict) -> 'Package':
        p = cls()
        p.deserialize(data)
        return p

    def __init__(self, pkgID: Optional[str] = None):
        self.id: str = ''
        self.development_mode: bool = False # -e
        self.repo: Repo = None
        self.constraints: List[Constraint] = []
        self.freezeVersion: Optional[Constraint] = None
        if pkgID is not None:
            if pkgID.startswith('-e '):
                self.development_mode = True
                pkgID=pkgID[3:]

            if os.path.isfile(pkgID):
                self.repo = WheelRepo(pkgID)
                self.id = self.repo.getID()
            elif pkgID.startswith('git+'):
                self.repo = GitRepo(pkgID)
                self.id = self.repo.pkgid
            else:
                repo = None
                if ' @ ' in pkgID:
                    pkgID, repo = pkgID.split('@', 1)
                    pkgID = pkgID.strip()
                    repo = repo.strip()
                m = self.REGEX_PACKAGENAME.match(pkgID)
                assert m is not None, f'Invalid package name {pkgID!r}'
                self.id = m[1]
                if repo is not None:
                    assert repo.startswith('git+')
                    self.repo = GitRepo(repo, knownPackageID=self.id)

                for cm in self.REGEX_CONSTRAINTS.findall(pkgID):
                    c = Constraint()
                    c.setEquality(cm[1])
                    c.setVersion(cm[2])
                    self.constraints += [c]

    def __str__(self) -> str:
        o = f'{self.id}'
        o += f' ({self.repo})' if self.repo is not None else ''
        if self.development_mode:
            o += ' [developer mode (-e)]'
        return o

    def serialize(self) -> dict:
        o = {}
        if self.development_mode:
            o['development'] = True
        if self.repo is not None:
            o['repo'] = self.repo.serialize()
        if len(self.constraints) > 0:
            o['constraints'] = []
            for constraint in self.constraints:
                o['constraints'] += [constraint.serialize()]
        if self.freezeVersion is not None:
            o['frozen-at'] = self.freezeVersion.serialize()
        return o

    def freezeAt(self, constraint: Constraint) -> None:
        self.freezeVersion = constraint

    def thaw(self) -> None:
        self.freezeVersion = None

    def deserialize(self, data: dict) -> None:
        self.development_mode = data.get('development', False)
        self.repo = None
        if 'repo' in data:
            #print(repr(data['repo']))
            rt = data['repo']['type']
            if rt == 'git':
                self.repo = GitRepo()
            elif rt == 'wheel':
                self.repo = WheelRepo()
            else:
                print(f"Error: Unknown repo.type={rt!r}")
            if self.repo is not None:
                self.repo.deserialize(data['repo'])
                #print(repr(self.repo), str(self.repo))
        if 'constraints' in data:
            for cdata in data['constraints']:
                c = Constraint()
                c.deserialize(cdata)
                self.constraints += [c]
        if 'frozen-at' in data:
            c = Constraint()
            c.deserialize(data['frozen-at'])
            self.freezeAt(c)


    def toRequirement(self) -> str:
        o = ''
        if self.development_mode:
            o += '-e '
        if self.repo is not None:
            o += self.repo.toRequirement(self)
        else:
            o += self.id
        if self.repo is None or self.repo.shouldDisplayConstraints():
            if self.freezeVersion is not None:
                o += self.freezeVersion.toRequirement()
            else:
                o += ','.join([x.toRequirement() for x in self.constraints])
        return o

    def toPipArgs(self) -> List[str]:
        o = []
        if self.development_mode:
            o += ['-e']
        if self.repo is not None:
            o += self.repo.toPipArgs(self)
        if self.repo is None or self.repo.shouldDisplayConstraints():
            if self.freezeVersion is not None:
                o += self.freezeVersion.toRequirement()
            else:
                o += ','.join([x.toRequirement() for x in self.constraints])
        return o
