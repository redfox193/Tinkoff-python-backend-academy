##
# make a file reader that reads .txt files
##
def read_txt_file(filename: str) -> str:
    # Just the implementation for reading txt files
    pass


content = read_txt_file('sample.txt')


##
# Display user's name and email
##
class UserProfile:
    def display_name(self):
        pass

    def display_email(self):
        pass


##
# Design a class that represents books reservation system
##
class ReservationSystem:
    def __init__(self):
        self.reservations = {}

    def reserve_book(self, user, book_id):
        # Code to reserve a book.
        self.reservations[(user, book_id)] = True

    def cancel_reservation(self, user, book_id):
        # Code to cancel the reservation.
        del self.reservations[(user, book_id)]
