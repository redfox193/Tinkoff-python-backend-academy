def add_tax(price):
    return price + (price * 0.2)


def discount(price):
    discounted = price - (price * 0.1)
    return discounted + (discounted * 0.2)


# # #
def get_username():
    while True:
        username = input("Enter username: ")
        if len(username) >= 5 and username.isalnum():
            return username
        else:
            print("Invalid username!")


def get_password():
    while True:
        password = input("Enter password: ")
        if len(password) >= 8:
            return password
        else:
            print("Invalid password!")


# # #
def circle_area(radius):
    return 3.14 * radius * radius


def rectangle_area(length, width):
    return length * width


def square_area(side):
    return side * side
