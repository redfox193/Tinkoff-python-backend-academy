def add_tax(price):
    return price + calculate_tax(price)


def discount(price):
    discounted = price - (price * 0.1)
    return discounted + calculate_tax(discounted)


def calculate_tax(price):
    return price * 0.2


# # #
def get_input(prompt, validation_func, error_msg):
    while True:
        data = input(prompt)
        if validation_func(data):
            return data
        else:
            print(error_msg)


username = get_input(
    "Enter username: ",
    lambda u: len(u) >= 5 and u.isalnum(),
    "Invalid username!"
)

password = get_input(
    "Enter password: ",
    lambda p: len(p) >= 8,
    "Invalid password!"
)
