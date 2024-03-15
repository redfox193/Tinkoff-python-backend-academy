# Create module that manages Users in db
class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def save_user_to_db(self):
        # database save operation here
        pass

    def fetch_user_from_db(self, user_id):
        # fetch user details from database
        pass


# Create module that prepare report in raw and html format
class Report:
    def __init__(self, data):
        self.data = data

    def generate_report(self) -> str:
        # logic to generate the report
        pass

    def render_to_html(self) -> str:
        # logic to render report to HTML
        pass


# Create module that calculates employee's pays
class Employee:
    def __init__(self, name, position, salary):
        self.name = name
        self.position = position
        self.salary = salary

    def calculate_pay(self, hours_worked):
        return self.salary * hours_worked
