import os

config = None
if os.path.exists('pycodya_config'):
    import pycodya_config as config


# Provide the autotest paths
DIR_GENERATED_TESTS= '.pycodya_tests' if not config else config.DIR_GENERATED_TESTS

# Provide the variable test
PYCODYA_VAR_NAME = 'CodyaTest' if not config else config.PYCODYA_VAR_NAME
