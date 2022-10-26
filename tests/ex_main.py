from ex_helpers import dada
from ex_import import CodyaTest
from tools.ex_tools import dodo

import random


@CodyaTest.function_tester
def do_something():
    return

@CodyaTest.function_tester
def add(a, b):
    do_something()
    random_unit(a)
    dada(1)
    
    return a + b + dodo(1) + 2

@CodyaTest.function_mock
def random_unit(a):
    return a + random.random()


class A():
    def __init__(self, number):
        self.number = number

    @CodyaTest.class_function_test
    def square(self):
        return self.number * self.number


if __name__ == "__main__":
    do_something()
    add(1, 2)
    A(12).square()
