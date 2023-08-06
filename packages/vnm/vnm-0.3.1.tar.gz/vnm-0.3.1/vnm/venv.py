import os
from subprocess import check_call
from vnm.consts import NAME, VAR_PREFIX
OLD_VENV_VAR = ''
def defined(varname):
    return varname in os.environ

def activate(venvdir) -> None:
    if os.name == 'nt':
        _activate_nt(venvdir)
    if os.name == 'posix':
        _activate_bash(venvdir)
    setEnv(f'_{VAR_PREFIX}_ACTIVE', '1')
    setEnv(f'_{VAR_PREFIX}_PROCESS', str(os.getpid()))

def deactivate(venvdir: str, nondestructive: bool = False) -> None:
    if os.name == 'nt':
        _deactivate_nt(venvdir, nondestructive)
    if os.name == 'posix':
        _deactivate_bash(venvdir, nondestructive)
    if defined(f'_{VAR_PREFIX}_ACTIVE'): unsetEnv(f'_{VAR_PREFIX}_ACTIVE')
    if defined(f'_{VAR_PREFIX}_PROCESS'): unsetEnv(f'_{VAR_PREFIX}_PROCESS')

def runFrom(venvdir: str, pythonfile: str, args: str):
    activate(venvdir)
    if os.path.isfile(pythonfile):
        pyexe = 'python.exe' if os.name == 'nt' else 'python'
        check_call([os.path.join(venvdir, 'bin', pyexe), pythonfile] + args)
    else:
        check_call(pythonfile + args)
    deactivate(venvdir)

def setEnv(varname: str, value: str) -> None:
    print(f'ENV: {varname} = {value}')
    os.environ[varname] = value

def unsetEnv(varname: str) -> None:
    print(f'ENV: {varname} (UNSET)')
    del os.environ[varname]

def getPrompt(venvdir) -> None:
    dirname = venvdir
    # Aspen shit
    if os.path.basename(venvdir) == '__':
        dirname = os.path.dirname(venvdir)
    dirname = os.path.basename(dirname)
    return f'({dirname}) '

def _activate_bash(venvdir: str) -> None:
    # unset irrelevant variables
    #deactivate nondestructive
    _deactivate_bash(venvdir, True)

    #VIRTUAL_ENV="__VENV_DIR__"
    #export VIRTUAL_ENV
    setEnv('VIRTUAL_ENV', venvdir)

    #_OLD_VIRTUAL_PATH="$PATH"
    setEnv('_OLD_VIRTUAL_PATH', os.environ['PATH'])
    #PATH="$VIRTUAL_ENV/__VENV_BIN_NAME__:$PATH"
    setEnv('PATH', os.environ['VIRTUAL_ENV']+'/bin:'+os.environ['PATH'])
    #export PATH

    # unset PYTHONHOME if set
    # this will fail if PYTHONHOME is set to the empty string (which is bad anyway)
    # could use `if (set -u; : $PYTHONHOME) ;` in bash
    #if [ -n "${PYTHONHOME:-}" ] ; then
    #    _OLD_VIRTUAL_PYTHONHOME="${PYTHONHOME:-}"
    #    unset PYTHONHOME
    #fi
    if defined('PYTHONHOME'):
        setEnv('_OLD_VIRTUAL_PYTHONHOME', os.environ['PYTHONHOME'])
        unsetEnv('PYTHONHOME')

    #if [ -z "${VIRTUAL_ENV_DISABLE_PROMPT:-}" ] ; then
    #    _OLD_VIRTUAL_PS1="${PS1:-}"
    #    if [ "x__VENV_PROMPT__" != x ] ; then
    #	PS1="__VENV_PROMPT__${PS1:-}"
    #    else
    #    if [ "`basename \"$VIRTUAL_ENV\"`" = "__" ] ; then
    #        # special case for Aspen magic directories
    #        # see http://www.zetadev.com/software/aspen/
    #        PS1="[`basename \`dirname \"$VIRTUAL_ENV\"\``] $PS1"
    #    else
    #        PS1="(`basename \"$VIRTUAL_ENV\"`)$PS1"
    #    fi
    #    fi
    #    export PS1
    #fi
    if not defined('VIRTUAL_ENV_DISABLE_PROMPT'):
        os.environ['_OLD_VIRTUAL_PS1'] = os.environ['PS1'] if defined('PS1') else '\\u@\\h \\w>'
        os.environ['PS1'] = getPrompt(venvdir)+os.environ.get('PS1', '\\u@\\h \\w>')

    # NOTE: This is already checked in _deactivate_posix(). Skipped
    # This should detect bash and zsh, which have a hash command that must
    # be called to get it to forget past commands.  Without forgetting
    # past commands the $PATH changes we made may not be respected
    #if [ -n "${BASH:-}" -o -n "${ZSH_VERSION:-}" ] ; then
    #    hash -r
    #fi

def _activate_nt(venvdir: str) -> None:
    setEnv('VIRTUAL_ENV', venvdir)

    if not defined('PROMPT'):
        setEnv('PROMPT', '$P$G')
    #if defined _OLD_VIRTUAL_PROMPT set PROMPT=%_OLD_VIRTUAL_PROMPT%
    if defined('_OLD_VIRTUAL_PROMPT'):
        setEnv('PROMPT', os.environ['_OLD_VIRTUAL_PROMPT'])
    #if defined _OLD_VIRTUAL_PYTHONHOME set PYTHONHOME=%_OLD_VIRTUAL_PYTHONHOME%
    if defined('_OLD_VIRTUAL_PYTHONHOME'):
        setEnv('PYTHONHOME', os.environ['_OLD_VIRTUAL_PYTHONHOME'])

    #set _OLD_VIRTUAL_PROMPT=%PROMPT%
    setEnv('_OLD_VIRTUAL_PROMPT', os.environ['PROMPT'])
    #set PROMPT=__VENV_PROMPT__%PROMPT%
    setEnv('PROMPT', getPrompt(venvdir) + os.environ['PROMPT'])
    #if defined PYTHONHOME set _OLD_VIRTUAL_PYTHONHOME=%PYTHONHOME%
    if defined('PYTHONHOME'):
        setEnv('_OLD_VIRTUAL_PYTHONHOME', os.environ['PYTHONHOME'])
        #set PYTHONHOME=
        unsetEnv('PYTHONHOME')

    #if defined _OLD_VIRTUAL_PATH set PATH=%_OLD_VIRTUAL_PATH%
    if defined('_OLD_VIRTUAL_PATH'):
        setEnv('PATH', os.environ['_OLD_VIRTUAL_PATH'])
    #if not defined _OLD_VIRTUAL_PATH set _OLD_VIRTUAL_PATH=%PATH%
    if not defined('_OLD_VIRTUAL_PATH'):
        setEnv('_OLD_VIRTUAL_PATH', os.environ['PATH'])

    #set PATH=%VIRTUAL_ENV%\__VENV_BIN_NAME__;%PATH%
    setEnv('PATH', os.environ['VIRTUAL_ENV']+'\\bin;'+os.environ['PATH'])

    #:END
    #if defined _OLD_CODEPAGE (
    #    "%SystemRoot%\System32\chcp.com" %_OLD_CODEPAGE% > nul
    #    set _OLD_CODEPAGE=
    #)

def _deactivate_nt(venvdir: str, nondestructive: bool = False) -> None:
    # venv currently doesn't have a deactivate script for NT, making it up
    # as we go.
    if defined('_OLD_VIRTUAL_PROMPT'):
        setEnv('PROMPT', os.environ['_OLD_VIRTUAL_PROMPT'])
        unsetEnv('_OLD_VIRTUAL_PROMPT')
    if not defined('PROMPT'):
        setEnv('PROMPT', '$P$G')
    if defined('_OLD_VIRTUAL_PYTHONHOME'):
        setEnv('PYTHONHOME', os.environ['_OLD_VIRTUAL_PYTHONHOME'])
        unsetEnv('_OLD_VIRTUAL_PYTHONHOME')
    if defined('_OLD_VIRTUAL_PATH'):
        setEnv('PATH', os.environ['_OLD_VIRTUAL_PATH'])
        unsetEnv('_OLD_VIRTUAL_PATH')
    if defined('VIRTUAL_ENV'):
        unsetEnv('VIRTUAL_ENV')

def _deactivate_bash(venvdir: str, nondestructive: bool = False) -> None:
    #deactivate () {
    # reset old environment variables
    #    if [ -n "${_OLD_VIRTUAL_PATH:-}" ] ; then
    #        PATH="${_OLD_VIRTUAL_PATH:-}"
    #        export PATH
    #        unset _OLD_VIRTUAL_PATH
    #    fi
    if defined('_OLD_VIRTUAL_PATH'):
        setEnv('PATH', os.environ['_OLD_VIRTUAL_PATH'])
        unsetEnv('_OLD_VIRTUAL_PATH')

    #    if [ -n "${_OLD_VIRTUAL_PYTHONHOME:-}" ] ; then
    #        PYTHONHOME="${_OLD_VIRTUAL_PYTHONHOME:-}"
    #        export PYTHONHOME
    #        unset _OLD_VIRTUAL_PYTHONHOME
    #    fi
    if defined('_OLD_VIRTUAL_PYTHONHOME'):
        setEnv('PYTHONHOME', os.environ['_OLD_VIRTUAL_PYTHONHOME'])
        unsetEnv('_OLD_VIRTUAL_PYTHONHOME')

    # This should detect bash and zsh, which have a hash command that must
    # be called to get it to forget past commands.  Without forgetting
    # past commands the $PATH changes we made may not be respected
    #    if [ -n "${BASH:-}" -o -n "${ZSH_VERSION:-}" ] ; then
    #        hash -r
    #    fi
    if defined('BASH') or defined('ZSH_VERSION'):
        # We can't run hash -r here, since hash won't affect the parent bash.
        print("IMPORTANT: You will need to run `hash -r` after this.")

    #    if [ -n "${_OLD_VIRTUAL_PS1:-}" ] ; then
    #        PS1="${_OLD_VIRTUAL_PS1:-}"
    #        export PS1
    #        unset _OLD_VIRTUAL_PS1
    #    fi
    if defined('_OLD_VIRTUAL_PS1'):
        os.environ['PS1'] = os.environ['_OLD_VIRTUAL_PS1']
        del os.environ['_OLD_VIRTUAL_PS1']

    #    unset VIRTUAL_ENV
    if defined('VIRTUAL_ENV'):
        unsetEnv('VIRTUAL_ENV')

    # We don't create this.
    #    if [ ! "${1:-}" = "nondestructive" ] ; then
    #        # Self destruct!
    #        unset -f deactivate
    #    fi

    #}
