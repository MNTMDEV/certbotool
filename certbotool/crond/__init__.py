import sys
from certbotool.crond.crond import CrondExecutable

def main():
    CrondExecutable(sys.argv)

if __name__ == '__main__':
    main()