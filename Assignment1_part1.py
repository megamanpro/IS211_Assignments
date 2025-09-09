# assignment1_part1.py

class ListDivideException(Exception):
    pass

def list_divide(numbers, divide=2):
    count = 0
    for n in numbers:
        if n % divide == 0:
            count += 1
    return count

def test_list_divide():

    try:
        assert list_divide([1, 2, 3, 4, 5]) == 2
        assert list_divide([2, 4, 6, 8, 10]) == 5
        assert list_divide([30, 54, 63, 98, 100], divide=10) == 2
        assert list_divide([]) == 0
        assert list_divide([1, 2, 3, 4, 5], 1) == 5
    except AssertionError:
        raise ListDivideException("list_divide failed one or more tests")
    else:
        print("test_list_divide passed successfully")

test_list_divide()

