from MachineModel import Machine
import sys


def REPL():
    pass


def RunCode(filename):
    interpeter = Machine(True)
    print(interpeter.load_file(filename))
    interpeter.execute(True)


if __name__ == "__main__":
    if (len(sys.argv) == 1):
        REPL()
    else:
        RunCode(sys.argv[1])
