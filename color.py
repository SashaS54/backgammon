from typing import Tuple


class Color:
    def __init__(self, r: int, g: int, b: int, a: int = 255):
        assert r <= 255 and g <= 255 and b <= 255 and a <= 255

        self.r: int = r
        self.g: int = g
        self.b: int = b
        self.a: int = a

    def toTuple(self) -> Tuple[int, int, int, int]:
        return self.r, self.g, self.b, self.a


Color.Red = Color(255, 0, 0)
Color.Green = Color(0, 255, 0)
Color.Blue = Color(0, 0, 255)
