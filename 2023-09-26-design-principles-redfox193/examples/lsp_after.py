from abc import abstractmethod


class Polygon:
    @abstractmethod
    def area(self):
        pass


class Rectangle(Polygon):
    def area(self):
        return self._width * self._height

    def __init__(self, width, height):
        self._width = width
        self._height = height

    def set_width(self, width):
        self._width = width

    def set_height(self, height):
        self._height = height


class Square(Polygon):
    def __init__(self, side_length):
        self._side_length = side_length

    def area(self):
        return self._side_length * self._side_length


def process(rect: Rectangle):
    rect.set_width(5)
    rect.set_height(4)
    assert rect._width * rect._height == 20


square = Square(3, 3)
process(square)  # This would fail the assertion because for a square, setting width also sets height.
