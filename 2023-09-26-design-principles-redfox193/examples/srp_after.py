# Create module that manages Users in db
class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


class UserDatabase:
    def save(self, user: User):
        # database save operation here
        pass

    def fetch(self, user_id) -> User:
        # fetch user details from database
        return User(...)

# Create module that prepare report in raw and html format
class Report:
    def __init__(self, data):
        self.data = data

    def generate(self):
        # logic to generate the report
        pass


class ReportRenderer:
    def render_to_html(self, report: Report):
        # logic to render report to HTML
        pass

# Create module that calculates employee's pays
class Employee:
    def __init__(self, name, position, salary):
        self.name = name
        self.position = position
        self.salary = salary


class PayCalculator:
    def calculate_pay(self, employee: Employee, hours_worked):
        return employee.salary * hours_worked
