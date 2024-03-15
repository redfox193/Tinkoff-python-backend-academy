class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class AreaCalculator:
    def calculate_area(self, rectangle: Rectangle):
        return rectangle.width * rectangle.height


class Circle:
    def __init__(self, radius):
        self.radius = radius


class AreaCalculator:
    def calculate_area(self, shape):
        if isinstance(shape, Rectangle):
            return shape.width * shape.height
        elif isinstance(shape, Circle):
            return 3.1415 * shape.radius * shape.radius

# # #
class ReportGenerator:
    def generate_report(self, data, format_type):
        if format_type == "CSV":
            return self._generate_csv_report(data)
        elif format_type == "JSON":
            return self._generate_json_report(data)
        elif format_type == "XML":
            return self._generate_xml_report(data)

    def _generate_csv_report(self, data):
        # Logic to generate CSV report.
        pass

    def _generate_json_report(self, data):
        # Logic to generate JSON report.
        pass

    def _generate_xml_report(self, data):
        # Logic to generate XML report.
        pass