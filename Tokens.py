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


token_map = {
    TokenEncoding.DATA_POINTER_RIGHT: ">",
    TokenEncoding.DATA_POINTER_LEFT: "<",
    TokenEncoding.INCREMENT_BYTE: "+",
    TokenEncoding.DECREMENT_BYTE: "-",
    TokenEncoding.OUTPUT_BYTE: ".",
    TokenEncoding.ACCEPT_INPUT: ",",
    TokenEncoding.LEFT_SQR_BRACE: "[",
    TokenEncoding.RIGHT_SQR_BRACE: "]",
        }

@dataclass
class Token:
    """
        ttype: TokenEncoding which is associated with some char
        location: the location of the token from the start of the file
    """
    ttype: TokenEncoding
    location: int

    def __repr__(self):
        return " ' "+token_map[self.ttype]+" '" + " "+ str(self.location)


