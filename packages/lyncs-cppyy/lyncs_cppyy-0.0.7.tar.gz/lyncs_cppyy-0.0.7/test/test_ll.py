from itertools import product
import numpy
from lyncs_cppyy import ll


def test_array_to_pointers():
    arr = numpy.arange((10))
    ptrs = ll.array_to_pointers(arr)
    assert (arr == list(ptrs)).all()

    arr = numpy.arange((4 * 3 * 2 * 1 * 2))
    arr = arr.reshape((4, 3, 2, 1, 2))
    ptrs = ll.array_to_pointers(arr)
    ranges = product(range(4), range(3), range(2), range(1), range(2))
    for r in ranges:
        val = ptrs
        for i in r:
            val = val[i]
        assert val == arr[r]


def test_to_pointer():
    arr = numpy.arange(10)
    ptr = ll.to_pointer(arr.__array_interface__["data"][0], "long*")
    ptr.reshape((10,))
    assert (arr == list(ptr)).all()


def test_assign():
    arr = numpy.arange(1)
    ptr = ll.to_pointer(arr.__array_interface__["data"][0], "long*")
    ptr.reshape((10,))
    ll.assign(ptr, 5)
    assert arr[0] == 5
