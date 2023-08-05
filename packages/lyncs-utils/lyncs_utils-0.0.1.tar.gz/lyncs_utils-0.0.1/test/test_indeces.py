from pytest import raises
from lyncs_utils import compact_indeces


def test_example():
    assert list(compact_indeces([1, 2, 4, 6, 7, 8, 10, 12, 13])) == [
        1,
        range(2, 7, 2),
        7,
        range(8, 13, 2),
        13,
    ]


def test_range():
    assert list(compact_indeces(range(10)))[0] == range(10)
    assert list(compact_indeces(range(10, 0, -1)))[0] == range(10, 0, -1)
    assert list(compact_indeces(range(2, 20, 2)))[0] == range(2, 20, 2)


def test_error():
    with raises(TypeError):
        list(compact_indeces(1))

    with raises(TypeError):
        list(compact_indeces([0.1, "foo"]))
