import os

config = None
if os.path.exists('pycodya_config'):
    import pycodya_config as config


# Provide the autotest paths
DIR_GENERATED_ROOT = '.pycodya'
DIR_GENERATED_TESTS = os.path.join(DIR_GENERATED_ROOT, 'tests')
CREDS_GENERATED_FILE = os.path.join(DIR_GENERATED_ROOT, 'creds.txt')
BRANCH_TOKEN_FILE = os.path.join(DIR_GENERATED_ROOT, 'branch.txt')

# Provide the variable test
PYCODYA_VAR_NAME = 'CodyaTest' if not config else config.PYCODYA_VAR_NAME
