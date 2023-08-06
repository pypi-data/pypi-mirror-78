from pytest import raises

from pybrary.func import (
    caller,
    todo,
    memo,
)


def callee():
    return caller()

def test_n_caller():
    assert callee() == 'test_n_caller'


def test_n_todo():
    class AbsCls:
        def abs_meth(self): todo(self)

    a = AbsCls()
    with raises(NotImplementedError) as x:
        a.abs_meth()
    assert str(x.value).strip() == '! abs_meth missing in AbsCls !'

def test_n_memo():
    class MemoTest:
        @memo
        def prop(self):
            return 'value'

    c = MemoTest()
    assert not hasattr(c, '_memo_prop')
    assert c.prop == c._memo_prop


if __name__=='__main__': test_n_memo()
