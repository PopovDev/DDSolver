from dataclasses import dataclass
from enum import Enum


class Operation(Enum):
    neg = '~'
    conjunc = '^'
    disjunc = 'v'


@dataclass
class Variable:
    text: str


@dataclass
class OperationNode:
    id: int
    content: list[ Operation | Variable]
    start: int
    end: int
