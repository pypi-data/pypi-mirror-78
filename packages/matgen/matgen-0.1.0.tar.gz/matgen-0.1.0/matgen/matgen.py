import numpy as np
from matast import Interpreter

class VerticalStacker(object):
    def __getitem__(self, mats):
        return np.vstack(mats)

class HorizontalStacker(object):
    def __getitem__(self, mats):
        return np.hstack(mats)

v_ = VerticalStacker()

h_ = HorizontalStacker()

def M_(text) -> np.ndarray:
    interpreter:Interpreter = Interpreter(text)
    return interpreter.interpret()


if __name__ == "__main__":
    print(v_[np.array([1,2,3]), h_[[[4,5],[4,5]], [[6],[6]]], np.zeros((2,3)), np.eye(3)])
    print(M_('[1 2 3; np.zeros((2, 2)), np.array([[1, 2]]).T]'))