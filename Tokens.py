from enum import Enum
from dataclasses import dataclass


class TokenEncoding(Enum):
    """Enum to map valid characters to integers"""
    DATA_POINTER_RIGHT = 0,
    DATA_POINTER_LEFT = 1,
    INCREMENT_BYTE = 2,
    DECREMENT_BYTE = 3,
    OUTPUT_BYTE = 4,
    ACCEPT_INPUT = 5,
    LEFT_SQR_BRACE = 6,
    RIGHT_SQR_BRACE = 7


@dataclass
class Token:
    """
        ttype: TokenEncoding which is associated with some char
        location: the location of the token from the start of the file
    """
    ttype: TokenEncoding
    location: int


