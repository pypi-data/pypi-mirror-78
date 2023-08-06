from functools import reduce
from operator import __add__

from pytest import raises

from pybrary.contract import (
    Contract,
    contract,
    PreError,
    ResultError,
    PostError,
)


class Adder(Contract):
    def pre(self, *a, **k):
        assert not k, "Adder doesn't support keywords arguments"
        assert len(a)>1, "Adder needs at least 2 arguments"
        for n in a:
            assert isinstance(n, (int, float)), f'invalid arg {type(n).__name__}({n}) for {self.name}, must be a number'

    def alt(self, *a, **k):
        r = 0
        for n in a: r+=n
        return r

    def post(self, r, *a, **k):
        if all(isinstance(n, int) for n in a):
            assert isinstance(r, int), f'wrong {self.name} result type : {type(r).__name__}, expected int'
        else:
            assert isinstance(r, float), f'wrong {self.name} result type : {type(r).__name__}, expected float'


def test_n_adder():
    @contract(Adder)
    def add1(*a):
        return sum(a)

    @contract(Adder)
    def add2(*a):
        return reduce(__add__, a)

    for add in (add1, add2):
        add(1, 2, 3)


def test_f_adder_arg():
    @contract(Adder)
    def add(*a):
        return sum(a)

    with raises(PreError): add(a=1)
    with raises(PreError): add(1)
    with raises(PreError): add(1, '2')


def test_f_adder_result():
    @contract(Adder)
    def add(*a):
        return sum(a)+1

    with raises(ResultError): add(2, 2)


def test_f_adder_post():
    @contract(Adder)
    def add(*a):
        return int(sum(a))

    with raises(PostError): add(2, 2.0)


if __name__=='__main__': test_f_adder_post()
