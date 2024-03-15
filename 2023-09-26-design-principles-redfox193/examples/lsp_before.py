class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    def set_width(self, width):
        self._width = width

    def set_height(self, height):
        self._height = height


class Square(Rectangle):
    def set_width(self, width):
        self._width = width
        self._height = width

    def set_height(self, height):
        self._width = height
        self._height = height


def update(rect: Rectangle):
    rect.set_width(5)
    rect.set_height(4)
    assert rect._width * rect._height == 20


square = Square(3, 3)
update(square)  # This would fail the assertion because for a square, setting width also sets height.
