from larning.testing import name
from pydantic import ValidationError, validate_arguments, ArbitraryTypeError
from pytest import raises
from typing import Union, List, Tuple, Set, Sequence
from typing import Iterable as typing_Iterable
from typing import Iterator as typing_Iterator


@name(validate_arguments, 0, globals())
def _():
    @validate_arguments
    def tested(a: int):
        return a

    assert tested(1) == 1
    assert tested(1.1) == 1
    with raises(ValidationError):
        tested("a")


@name(validate_arguments, 1, globals())
def _():
    @validate_arguments
    def tested(a) -> int:
        return a

    assert tested(1) == 1
    assert tested(1.1) == 1.1
    assert tested("a") == "a"


@name(validate_arguments, 2, globals())
def _():
    @validate_arguments
    def tested(a: Union[int, str]):
        return a

    assert tested(1) == 1
    assert tested(1.1) == 1
    assert tested("a") == "a"


@name(validate_arguments, 3, globals())
def _():
    @validate_arguments
    def tested(a: Union[str, int]):
        return a

    assert tested(1) == "1"
    assert tested(1.1) == "1.1"
    assert tested("a") == "a"


@name(validate_arguments, "list", globals())
def _():
    @validate_arguments
    def tested(a: List[int]):
        return a

    # basic
    assert tested([1.1]) == [1]
    assert tested((1.1,)) == [1]
    assert tested({1.1}) == [1]
    # empty
    assert tested([]) == []
    assert tested(tuple()) == []
    assert tested(set()) == []
    #
    with raises(ValidationError):
        assert tested({None}) == [None]


@name(validate_arguments, "tuple", globals())
def _():
    @validate_arguments
    def tested(a: Tuple[int]):
        return a

    # basic
    assert tested([1.1]) == (1,)
    assert tested((1.1,)) == (1,)
    assert tested({1.1}) == (1,)
    # empty
    with raises(ValidationError):
        assert tested([]) == tuple()
    with raises(ValidationError):
        assert tested(tuple()) == tuple()
    with raises(ValidationError):
        assert tested(set()) == tuple()


@name(validate_arguments, "set", globals())
def _():
    @validate_arguments
    def tested(a: Set[int]):
        return a

    # basic
    assert tested([1.1]) == {1}
    assert tested((1.1,)) == {1}
    assert tested({1.1}) == {1}
    # empty
    assert tested([]) == set()
    assert tested(tuple()) == set()
    assert tested(set()) == set()


@name(validate_arguments, "typing_Iterable", globals())
def _():
    @validate_arguments
    def tested(a: typing_Iterable[int]):
        return a

    # basic
    assert list(tested([1.1])) == [1.1]
    assert list(tested({1.1})) == [1.1]
    assert list(tested((1.1,))) == [1.1]
    # empty
    assert list(tested([])) == []
    assert list(tested(set())) == []
    assert list(tested((tuple()))) == []
    # type
    assert type(tested([])) == type(iter([]))
    assert type(tested(set())) == type(iter(set()))
    assert type(tested((tuple()))) == type(iter(tuple()))


@name(validate_arguments, "typing_Iterator", globals())
def _():
    with raises(TypeError):

        @validate_arguments
        def tested(a: typing_Iterator[int]):
            return a


@name(validate_arguments, "sequence", globals())
def _():
    @validate_arguments
    def tested(a: Sequence[int]):
        return a

    # basic
    assert tested([1.1]) == [1]
    assert tested({1.1, 2}) == {2, 1}
    assert tested((1.1, 2)) == (1, 2)
    # empty
    assert tested([]) == []
    assert tested(set()) == set()
    assert tested((tuple())) == tuple()
