"""pycodya.

Usage:
  pycodya <actions>  

Options:
  -h --help     Show this screen.
  --version     Show version.
  actions       alltests: test everything


Actions:
 login         Login to the codya
 logout        Remove the session
 projects      Connect to the right project and branch
 alltests      Run all alltests for that project

"""

from docopt import docopt
from pycodya.run_tests import run_tests
from pycodya.codya_api import CodyaApi


def main():
    arguments = docopt(__doc__, version="0.2.1a")

    if arguments['<actions>'] == 'alltests':
        run_tests()
    elif arguments['<actions>'] == 'login':
        CodyaApi().login()
    elif arguments['<actions>'] == 'logout':
        CodyaApi().logout()
    elif arguments['<actions>'] == 'projects':
        CodyaApi().projects()
    elif arguments['<actions>'] == 'pull':
        CodyaApi().pull_data() 
    


if __name__ == '__main__':
    main()
    

