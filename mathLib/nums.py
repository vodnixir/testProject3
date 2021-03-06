import doctest


def plus(a, b):
    """
    возвращает сумму аргументов a и b

    :param a:
    :param b:
    :return:

    >>> plus(2,3)
    5
    >>> plus(4.5,5.5)
    10.0

    """
    return a + b


def minus(a, b):
    """
    возвращает разность аргументов a и b

    :param a:
    :param b:
    :return:

    >>> minus(3,2)
    1
    >>> minus(5,7)
    -2
    """
    return a - b


def multy(a, b):
    """
    возвращает произведение аргументов a и b

    :param a:
    :param b:
    :return:

    >>> multy(2,8)
    16
    >>> multy(4,-3)
    -12
    """
    return a * b


def div(a, b):
    """
    возвращает аргументов a и b
    :param a:
    :param b:
    :return:

    >>> div(8,4)
    2.0
    >>> div(7,2)
    3.5
    """
    return a / b


if __name__ == '__main__':
    print(f"привет из модуля nums.py,__name__={__name__}")
    assert (plus(2, 3) == 5)
    doctest.testmod()
