from functools import reduce

def factors(n, ordered=True):
    """Get factors of a number in a list.

    Parameters:
    n (int): The number that you want to get the factors of.
    ordered (bool): Whether you want the output to be ordered from smallest to largest. Setting this value to false will marginally increase the speed of the function. (DEFAULT: True)

    Returns:
    list: List of the factors of n.
    """
    if ordered:
        return list(set(reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0))))
    else:
        return list(reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))