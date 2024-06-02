from MachineModel import Machine
import sys


def REPL():
    # TODO
    pass


def RunCode(filename):
    interpeter = Machine(True, False)
    interpeter.load_file(filename)
    interpeter.execute()


if __name__ == "__main__":
    if (len(sys.argv) == 1):
        REPL()
    else:
        RunCode(sys.argv[1])
