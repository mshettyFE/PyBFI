from MachineModel import Machine
import sys


def REPL():
    pass


def RunCode(filename):
    interpeter = Machine(True,False)
    interpeter.load_file(filename)
#    [print(item) for item in interpeter.program]
    interpeter.execute()
#    for index, val in enumerate(interpeter.data):
#        print(index, val)


if __name__ == "__main__":
    if (len(sys.argv) == 1):
        REPL()
    else:
        RunCode(sys.argv[1])
