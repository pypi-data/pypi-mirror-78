# pylint: disable=unused-variable

#Import numpy
import numpy as np

def empty_list(length, dimensions=1):
    """Create an empty list with specified length and dimensions.

    Parameters:
    length (int): Length of each side of the array.
    dimensions (int): Dimensions of the array. (DEFAULT: 1)

    Returns:
    list: List filled with 0.0s.
    """
    a = (length,)
    for i in range(1,dimensions):
        a = a + (length,)

    return (np.zeros(a)).tolist()

def flatten_list(l):
    """Flatten a multidimensinoal list to a 1 dimensional list.

    Parameters:
    l (list): The list that you want to flatten.

    Returns:
    list: ! dimensional list.
    """
    try:
        return flatten_list(l[0]) + (flatten_list(l[1:]) if len(l) > 1 else []) if type(l) is list else [l]
    except IndexError:
        return []


def list_total(l):
    """Add up all the ints / floats in a multidimensional list.

    Parameters:
    l (list): The list that you want to get the sum of.

    Returns:
    float: Total of the list's elements.
    """
    try:
        return float(sum(flatten_list(l)))
    except TypeError:
        return 0