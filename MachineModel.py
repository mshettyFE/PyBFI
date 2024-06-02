from Tokens import TokenEncoding, Token, token_map
from CharacterException import CharacterException
from collections import deque
from typing import List


data_size = 30000


class Machine:

    def __init__(self, afail_hard: bool = False, a_verbose: bool = False):
        """
            virtual machine upon which Brainfuck is run on
            self.fail_hard: if an error occurs, the machine resets to some known state.
            Fail_hard denotes how the machine should fail. It either hard resets, or soft resets
        """
        global data_size
        self.program_loaded: bool = False  # If False, machine refuses to run
        self.fail_hard: bool = afail_hard
        self.verbose = a_verbose
        self.instruction_pointer: int = 0  # Index into program memory
        self.program: List[Token] = []  # List of tokens of program to be run
        self.data: List[str] = [0]*data_size  # Machine RAM in bytes
        self.data_pointer: int = 0  # Throws error if out of data bounds
        self.bracket_map: dict[int, int] = {}  # maps bracket locations

    def status(self):
        print("prg_ptr: "+str(self.instruction_pointer))
        print("cur_program: "+str(self.program[self.instruction_pointer]))
        print("data_ptr: "+str(self.data_pointer))
        print("data: "+str(self.data[self.data_pointer]))
        print("bracket_map: "+str(self.bracket_map))
        print("\n\n")

    def panic(self, expt: CharacterException):
        if (self.fail_hard):
            self.hard_reset()
        else:
            self.soft_reset()
        raise expt

    def soft_reset(self):
        """Resets everything except the data and the data pointer"""
        self.program_loaded = False
        self.instruction_pointer = 0
        self.program = []
        self.bracket_map = {}

    def hard_reset(self):
        """Soft resets, and also clears out data/ resets data pointer"""
        self.soft_reset()
        self.data = [0] * data_size
        self.data_pointer = 0

    def strip_code(self, program_bytes: str):
        accepted_tokens = ('>', '<', '+', '-', '.', ',',
                           '[', ']')  # Valid characters
        return ''.join([byte for byte in program_bytes if byte in accepted_tokens])

    def add_to_mapping(self, left_token: Token, right_token: Token):
        self.bracket_map[left_token.location] = right_token.location
        self.bracket_map[right_token.location] = left_token.location

    def load_string(self, program_bytes: str):
        if (len(program_bytes) == 0):
            raise CharacterException("Code is empty. C'mon, do something...")
        bracket_stack = deque()
        for index, byte in enumerate(program_bytes):
            # valid_characters: ('>', '<', '+', '-', '.', ',', '[', ']')
            match byte:
                case '>':
                    self.program.append(
                        Token(TokenEncoding.DATA_POINTER_RIGHT, index))
                case '<':
                    self.program.append(
                        Token(TokenEncoding.DATA_POINTER_LEFT, index))
                case '+':
                    self.program.append(
                        Token(TokenEncoding.INCREMENT_BYTE, index))
                case '-':
                    self.program.append(
                        Token(TokenEncoding.DECREMENT_BYTE, index))
                case '.':
                    self.program.append(
                        Token(TokenEncoding.OUTPUT_BYTE, index))
                case ',':
                    self.program.append(
                        Token(TokenEncoding.ACCEPT_INPUT, index))
                case '[':
                    new_token = Token(TokenEncoding.LEFT_SQR_BRACE, index)
                    bracket_stack.append(new_token)
                    self.program.append(new_token)
                case ']':
                    closing_brace_token = Token(
                        TokenEncoding.RIGHT_SQR_BRACE, index)
                    if (len(bracket_stack) == 0):
                        mismatch_bracket_exp = CharacterException(
                            "No associated open bracket for close bracket", index)
                        self.panic(mismatch_bracket_exp)
                    else:
                        associated_bracket = bracket_stack.pop()  # Grab corresponding open brace
                        # Save two tuples that map the braces to each other
                        self.add_to_mapping(
                            associated_bracket, closing_brace_token)
                        # Add to tally of tokens
                        self.program.append(closing_brace_token)
                case _:
                    continue  # Invalid character reached. Ignore. Note this includes whitespace!
        if (len(bracket_stack) != 0):
            tally = ""
            for key in bracket_stack:
                tally += "\t" + str(key)+"\n"
            err = CharacterException(
                "Unclosed brackets at the following lines:"+tally)
            self.panic(err)

        self.program_loaded = True  # Congrajlashins! Can exit now
        return self.program

    def load_file(self, file_name: str):
        with open(file_name, 'r') as f:
            program_bytes = f.read()
        return self.load_string(program_bytes)

    def check_data_pointer_validity(self, location) -> bool:
        if ((self.data_pointer < 0) or (self.data_pointer >= data_size)):
            expt = CharacterException(
                "Data pointer out of bounds. Currently at " + str(self.data_pointer), location)
            self.panic(expt)
        return True

    def get_input(self) -> str:
        """
            Wait for user input. After hitting enter, grabs first character and discards the rest. Doesn't do empty input
        """
        data = ""
        while (len(data) == 0):
            data = input()
        return data[0]

    def execute(self):
        if not (self.program_loaded):
            raise Exception("Program is currently not loaded")
        global data_size
        program_length = len(self.program)
        while ((self.instruction_pointer >= 0) and (self.instruction_pointer < program_length)):
            cur_token = self.program[self.instruction_pointer]
#            print(cur_token, self.data_pointer, self.data[self.data_pointer])
            match cur_token.ttype:
                case TokenEncoding.DATA_POINTER_RIGHT:
                    self.data_pointer += 1
                case TokenEncoding.DATA_POINTER_LEFT:
                    self.data_pointer -= 1
                case TokenEncoding.INCREMENT_BYTE:
                    #                    if self.check_data_pointer_validity(cur_token.location):
                    self.data[self.data_pointer] += 1
                case TokenEncoding.DECREMENT_BYTE:
                    #                    if self.check_data_pointer_validity(cur_token.location):
                    self.data[self.data_pointer] -= 1
                case TokenEncoding.OUTPUT_BYTE:
                    #                    if self.check_data_pointer_validity(cur_token.location):
                    out_byte = self.data[self.data_pointer]
                    print(str(out_byte), end='', flush=True)
                case TokenEncoding.ACCEPT_INPUT:
                    byte_to_write = self.get_input()
#                    if self.check_data_pointer_validity(cur_token.location):
                    self.data[self.data_pointer] = byte_to_write
                case TokenEncoding.LEFT_SQR_BRACE | TokenEncoding.RIGHT_SQR_BRACE:
                    #                    if self.check_data_pointer_validity(cur_token.location):
                    cur_data = self.data[self.data_pointer]
                    if (cur_data == 0):
                        self.instruction_pointer = self.bracket_map[cur_token.location]
                case _:
                    expt = CharacterException(
                        "Invalid token found: " + str(cur_token.ttype), cur_token.location)
                    self.panic(expt)
            self.instruction_pointer += 1
        if (self.verbose):
            print("\n\nProgram terminated Successfully")
        if (self.fail_hard):
            self.hard_reset()
        else:
            self.soft_reset()
