class Color:
    def __init__(self, r: int, g: int, b: int, a: int = 255):
        assert r <= 255 and g <= 255 and b <= 255 and a <= 255

        self.r = r
        self.g = g
        self.b = b
        self.a = a


Color.Red = Color(255, 0, 0)
Color.Green = Color(0, 255, 0)
Color.Blue = Color(0, 0, 255)
