from pybrary.contract import Contract, contract

from pybrary.func import fqn


def expect(obj, name):
    assert fqn(obj)==name, f'\n ! expected {name}\n !      got {fqn(obj)}'


def test_n_fqn():
    expect(contract, 'pybrary.contract.contract')
    expect(Contract, 'pybrary.contract.Contract')
    expect(Contract.pre, 'pybrary.contract.pre')
    expect(Contract(expect), 'pybrary.contract.Contract')
    expect(Contract(expect).pre, 'pybrary.contract.pre')


def test_c_fqn():
    from os import listdir
    from sys import path
    expect(42, 'int')
    expect({}, 'dict')
    expect(listdir, 'listdir')
    expect(path, 'list')


if __name__=='__main__': test_c_fqn()
