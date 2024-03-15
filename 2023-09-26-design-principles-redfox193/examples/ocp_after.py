from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self):
        pass


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.1415 * self.radius * self.radius

class AreaCalculator:
    def calculate_area(self, shape: Shape):
        return shape.area()


# # #
# Define the ReportStrategy interface.
class ReportStrategy(ABC):
    @abstractmethod
    def generate(self, data):
        pass


class CsvReportStrategy(ReportStrategy):
    def generate(self, data):
        # Logic to generate CSV report.
        pass


class JsonReportStrategy(ReportStrategy):
    def generate(self, data):
        # Logic to generate JSON report.
        pass


class XmlReportStrategy(ReportStrategy):
    def generate(self, data):
        # Logic to generate XML report.
        pass


class ReportGenerator:
    def __init__(self, strategy: ReportStrategy):
        self._strategy = strategy

    def generate_report(self, data):
        return self._strategy.generate(data)
