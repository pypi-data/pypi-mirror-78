import enum
import re
import sys
import urllib.parse
import string
from typing import List, Optional
from vnm.repos.repo import Repo
class EGitRefType(enum.IntEnum):
    NONE   = enum.auto()
    BRANCH = enum.auto()
    TAG    = enum.auto()
    COMMIT = enum.auto()
    BLOB   = enum.auto()

class GitRepo(Repo):
    TYPEID = 'git'
    REGEX_FORMAT_1 = re.compile(r'^git\+(?P<uri>[^@#]+)(@(?P<refid>[a-z0-9/\-_]+))?')
    REGEX_FORMAT_2 = re.compile(r'^git\+(?P<uri>[^@#]+)(@(?P<refid>[a-z0-9/\-_]+))?#egg=(?P<pkgid>[a-z0-9_\-]+)')
    REGEX_REFID_COMMON_TAGS = re.compile(r'^[vV]?(\d+\.)+\d+(\-(rc|alpha|beta)?\d*)$')
    LONG_COMMIT_LEN = 40 # 58186079583c71760fd6b1950bee5fa92e3cd364
    SHORT_COMMIT_LEN = 7 # I think
    def __init__(self, uri: str = "", knownPackageID: Optional[str] = None):
        self.uri: str = ''
        self.pkgid: str = knownPackageID
        self.refid: Optional[str] = None
        self.reftype: EGitRefType = EGitRefType.NONE

        super().__init__()

        def _err_bad_uri_format():
            print(f'Improper git repo definition string: {uri}')
            print(f'Proper format: git+schema://uri/to/repo.git[@branch-or-commit]#egg=packageid')
            print(f'               git+username@server:/path/to/repo.git[@branch-or-commit]#egg=packageid')
            sys.exit(1)

        if uri != '':
            if '#egg=' in uri:
                m = self.REGEX_FORMAT_2.match(uri)
                if m is None:
                    _err_bad_uri_format()
                else:
                    self.uri = m.group('uri')
                    if self.pkgid is None:
                        self.pkgid = m.group('pkgid')
                    self.refid = m.group('refid')
            else:
                m = self.REGEX_FORMAT_1.match(uri)
                if m is None:
                    _err_bad_uri_format()
                else:
                    self.pkgid = None
                    self.uri = m.group('uri')
                    self.refid = m.group('refid')
                    #print(self.refid)
                    uriinfo = urllib.parse.urlparse(self.uri)
                    if self.pkgid is None:
                        self.pkgid = uriinfo.path.split('/')[-1].split('.')[0]
            if self.refid is not None:
                # If the refid is all hex and the length of commits sha1s...
                if len(self.refid) == self.LONG_COMMIT_LEN and all(x in string.hexdigits for x in self.refid):
                    self.reftype = EGitRefType.COMMIT
                elif self.REGEX_REFID_COMMON_TAGS.match(self.refid) is not None:
                    self.reftype = EGitRefType.TAG
                else:
                    self.reftype = EGitRefType.BRANCH


    def __str__(self):
        o = f'Git: {self.uri}'
        if self.reftype != EGitRefType.NONE:
            o += ' @ '
            if self.reftype == EGitRefType.BLOB:
                o += f'blob {self.refid}'
            if self.reftype == EGitRefType.BRANCH:
                o += f'branch {self.refid!r}'
            if self.reftype == EGitRefType.TAG:
                o += f'tag {self.refid!r}'
            if self.reftype == EGitRefType.COMMIT:
                o += f'commit {self.refid}'
        return o

    def serialize(self) -> dict:
        data = super().serialize()
        data['uri'] = self.uri
        if self.reftype != EGitRefType.NONE:
            data[self.reftype.name.lower()] = self.refid
        return data

    def deserialize(self, data: dict) -> None:
        super().deserialize(data)
        self.uri = data['uri']
        if 'branch' in data:
            self.reftype = EGitRefType.BRANCH
            self.refid = data['branch']
        elif 'tag' in data:
            self.reftype = EGitRefType.TAG
            self.refid = data['tag']
        elif 'commit' in data:
            self.reftype = EGitRefType.COMMIT
            self.refid = data['commit']

    def toRequirement(self, parent: 'Package') -> str:
        line = 'git+'+self.uri
        if self.refid is not None:
            line += f'@{self.refid}'
        line += f'#egg={parent.id}'
        return line

    def toPipArgs(self, parent: 'Package') -> List[str]:
        return [self.toRequirement(parent)]

    def shouldDisplayConstraints(self) -> bool:
        return False
