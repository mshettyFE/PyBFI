from enum import Enum
from dataclasses import dataclass


class TokenEncoding(Enum):
    DATA_POINTER_RIGHT = 1,
    DATA_POINTER_LEFT = 2,
    INCREMENT_BYTE = 3,
    DECREMENT_BYTE = 4,
    OUTPUT_BYTE = 5,
    ACCEPT_INPUT = 6,
    LEFT_SQR_BRACE = 7,
    RIGHT_SQR_BRACE = 8


@dataclass
class Token:
    ttype: TokenEncoding
    location: int
