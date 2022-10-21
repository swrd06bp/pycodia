# pycodia


### Utilization

```python
from pycodia import Codia

CodiaTest = Codia()


@CodiaTest.function_tester
def do_something():
    # code here

@CodiaTest.function_mock
def do_something_else():
    # code here

```

### Run tests
```sh
python3 run_tests.py
```



