from typing import List
from wheel.wheelfile import WheelFile
import os
import shutil
import tempfile
import urllib.request
from vnm.repos.repo import Repo

class WheelRepo(Repo):
    TYPEID = 'wheel'

    def __init__(self, uri: str = ""):
        self.uri: str = uri

    def __str__(self):
        return f'Wheel: {self.uri}'

    def serialize(self) -> dict:
        data = super().serialize()
        data['uri'] = self.uri
        return data

    def deserialize(self, data: dict) -> None:
        super().deserialize(data)
        self.uri = data['uri']

    def toRequirement(self, parent: 'Package') -> str:
        return self.uri

    def toPipArgs(self, parent: 'Package') -> List[str]:
        return [self.uri]

    def shouldDisplayConstraints(self) -> bool:
        return False

    def getID(self) -> str:
        path = self.uri
        ntf = None
        try:
            if not os.path.isfile(self.uri):
                ntf = tempfile.NamedTemporaryFile(delete=False)
                path = ntf.name
                with urllib.request.urlopen(self.uri) as response:
                    shutil.copyfileobj(response, ntf)
            with WheelFile(path) as wf:
                return wf.parsed_filename.group('namever')
        finally:
            if ntf is not None:
                ntf.close()
                if os.path.isfile(path):
                    os.remove(path)
