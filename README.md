# pycodya


### Utilization

```python
from pycodya import Codya

CodyaTest = Codya()


@CodyaTest.function_tester
def do_something():
    # code here
    return

@CodyaTest.function_mock
def do_something_else():
    # code here
    return
```

### Run tests
```sh
python3 run_tests.py
```



