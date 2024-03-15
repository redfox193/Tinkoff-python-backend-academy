def parse_input(data):
    try:
        result = data.split(":")
        return {
            "key": result[0].strip(),
            "value": int(result[1].strip())
        }
    except:
        raise ValueError("Invalid data format!")


def has_unique_chars(s):
    char_list = []
    for char in s:
        if char in char_list:
            return False
        else:
            char_list.append(char)
    return True


class NumberProcessor:
    def __init__(self, numbers):
        self.numbers = numbers

    def filter_evens(self):
        self.numbers = [number for number in self.numbers if number % 2 == 0]

    def square_numbers(self):
        self.numbers = [number * number for number in self.numbers]

    def process_numbers(self):
        self.filter_evens()
        self.square_numbers()
        return self.numbers


def process_numbers_before():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    processor = NumberProcessor(numbers)
    squared_evens = processor.process_numbers()
    print(squared_evens)


def check_user(user):
    if user.is_active:
        if user.has_permission:
            if user.is_admin:
                print("User is an active admin with permissions.")
            else:
                print("User is active and has permissions but is not an admin.")
        else:
            if user.is_admin:
                print("User is an active admin but lacks permissions.")
            else:
                print("User is active but lacks permissions and is not an admin.")
    else:
        print("User is not active.")