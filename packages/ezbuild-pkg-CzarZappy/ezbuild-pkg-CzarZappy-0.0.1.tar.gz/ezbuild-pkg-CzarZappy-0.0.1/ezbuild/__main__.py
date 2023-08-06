import sys

from ezbuild import app

# MAIN entry point

if __name__ == "__main__":
    print('[ZBUILD] Number of arguments:', len(sys.argv), 'arguments.')
    print('[ZBUILD] Argument List:', str(sys.argv))
    app.run(sys.argv[1:])
