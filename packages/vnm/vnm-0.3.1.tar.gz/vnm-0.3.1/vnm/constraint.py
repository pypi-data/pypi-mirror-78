import enum
from typing import Optional
class EEqualityType(enum.IntEnum):
    EQUAL                 = enum.auto()
    GREATER_THAN_OR_EQUAL = enum.auto()
    LESS_THAN_OR_EQUAL    = enum.auto()
    LESS_THAN             = enum.auto()
    GREATER_THAN          = enum.auto()

    @staticmethod
    def ToRequirement(val):
        if val == EEqualityType.EQUAL:
            return '=='
        if val == EEqualityType.GREATER_THAN_OR_EQUAL:
            return '>='
        if val == EEqualityType.LESS_THAN_OR_EQUAL:
            return '<='
        if val == EEqualityType.GREATER_THAN:
            return '>'
        if val == EEqualityType.LESS_THAN:
            return '<'
        return '??'

class Constraint(object):
    def __init__(self, txt: Optional[str] = None):
        self.version: str = ''
        self.equality: EEqualityType = EEqualityType.EQUAL
        self.frozen: bool = False

    def setVersion(self, v: str) -> None:
        self.version = v

    def setEquality(self, eq: str) -> None:
        if eq in ('==', 'eq'):
            self.equality = EEqualityType.EQUAL
        elif eq in ('>=', 'gte'):
            self.equality = EEqualityType.GREATER_THAN_OR_EQUAL
        elif eq in ('<=', 'lte'):
            self.equality = EEqualityType.LESS_THAN_OR_EQUAL
        elif eq in ('>', 'gt'):
            self.equality = EEqualityType.GREATER_THAN
        elif eq in ('<', 'lt'):
            self.equality = EEqualityType.LESS_THAN

    def toRequirement(self) -> str:
        o = ''
        o += EEqualityType.ToRequirement(self.equality)
        o += str(self.version)
        return o

    def serialize(self) -> dict:
        o = {
            'comparison': EEqualityType.ToRequirement(self.equality),
            'version': self.version,
        }
        if self.frozen:
            o['frozen'] = True
        return o

    def deserialize(self, data: dict) -> None:
        if isinstance(data, list):
            self.setEquality(data[0])
            self.setVersion(data[1])
        else:
            self.setVersion(data['version'])
            self.setEquality(data['comparison'])
            self.frozen = data.get('frozen', False)
