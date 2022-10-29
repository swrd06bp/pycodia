"""pycodya.

Usage:
  pycodya run <actions>  

Options:
  -h --help     Show this screen.
  --version     Show version.
  actions       alltests: test everything

"""

from docopt import docopt
from pycodya.run_tests import run_tests


def main():
    arguments = docopt(__doc__, version="0.1.1")
    print(arguments)

    if arguments['<actions>'] == 'alltests':
        run_tests()


if __name__ == '__main__':
    main()
    

