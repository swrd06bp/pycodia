# pycodya


### Utilization

```python
from pycodya import Codya

CodyaTest = Codya()


@CodyaTest.function_tester
def do_something():
    # code here

@CodyaTest.function_mock
def do_something_else():
    # code here

```

### Run tests
```sh
python3 run_tests.py
```



