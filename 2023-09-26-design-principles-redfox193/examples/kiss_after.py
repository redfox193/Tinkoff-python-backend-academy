def parse_input(data):
    key, value = data.split(":")
    return {"key": key.strip(), "value": int(value.strip())}


def has_unique_chars_after(s):
    return len(s) == len(set(s))


def process_numbers_after():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    squared_evens = [x * x for x in numbers if x % 2 == 0]
    print(squared_evens)


def check_user(user):
    if not user.is_active:
        print("User is not active.")
        return

    if not user.has_permission and not user.is_admin:
        print("User is active but lacks permissions and is not an admin.")
        return

    if not user.has_permission and user.is_admin:
        print("User is an active admin but lacks permissions.")
        return

    if user.has_permission and not user.is_admin:
        print("User is active and has permissions but is not an admin.")
        return

    print("User is an active admin with permissions.")
