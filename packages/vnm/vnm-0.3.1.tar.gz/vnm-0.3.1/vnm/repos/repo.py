from typing import List
class Repo(object):
    TYPEID = ''
    def __init__(self):
        pass

    def serialize(self) -> dict:
        return {'type': self.TYPEID}

    def deserialize(self, data: dict) -> None:
        return

    def toRequirement(self, parent: 'Package') -> str:
        return ''

    def toPipArgs(self, parent: 'Package') -> List[str]:
        return []

    def shouldDisplayConstraints(self) -> bool:
        return True
