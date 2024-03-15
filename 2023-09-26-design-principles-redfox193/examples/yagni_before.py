##
# make a file reader that reads .txt files
##

class FileReader:
    def read_txt(self, filename: str) -> str:
        # Implementation for reading txt files
        pass

    def read_pdf(self, filename: str) -> str:
        # Implementation for reading pdf files
        pass

    def read_docx(self, filename) -> str:
        # Implementation for reading docx files
        pass

    def read_xls(self, filename) -> str:
        # Implementation for reading xls files
        pass


##
# Display user's name and email
##
class UserProfile:
    def display_name(self):
        pass

    def display_email(self):
        pass

    def display_address(self):  # Not currently needed
        pass

    def display_phone_number(self):  # Not currently needed
        pass

    def display_social_links(self):  # Not currently needed
        pass


##
# Design a class that represents books reservation system
##
class ReservationSystem:
    def __init__(self):
        self.reservations = {}

    def reserve_book_copy(self, user, book_copy_id, pickup_time):
        # Code to reserve a specific copy of the book at a specific time.
        self.reservations[(user, book_copy_id)] = pickup_time

    def reserve_multiple_copies(self, user, book_ids, pickup_times):
        for book_id, pickup_time in zip(book_ids, pickup_times):
            self.reserve_book_copy(user, book_id, pickup_time)

    def cancel_reservation(self, user, book_copy_id):
        # Code to cancel the reservation.
        del self.reservations[(user, book_copy_id)]
