from mathLib import nums
import cmath


class SchoolClass:
    def __init__(self, cntPup, numClass):
        self.cntPup = cntPup
        self.numClass = numClass

    def __str__(self):
        return (f"SchoolClass(cntPup={self.cntPup},numClass={self.numClass})")

    def __repr__(self):
        return (f"SchoolClass({self.cntPup},{self.numClass})")


def proba():
    print("proba")
    proba2()
    i = 5
    s = "hello"
    print(f"s(s)={s} s(r)={s!r}")
    c = SchoolClass(7, 8)
    c2 = SchoolClass(6,9)
    print(f"c = {c!r}")
    print(f"c2 = {c2!r}")

def proba2():
    print("proba2")


if __name__ == '__main__':
    print(f"привет из модуля calculator.py, __name__={__name__}")

proba()
