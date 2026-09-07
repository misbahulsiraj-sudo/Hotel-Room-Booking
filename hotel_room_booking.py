import json
import os
from datetime import datetime


class Room:
    def __init__(self, room_number, room_type, price_per_night):
        self.room_number = room_number
        self.room_type = room_type
        self.price_per_night = price_per_night
        self.is_booked = False

    def to_dict(self):
        return {
            "room_number": self.room_number,
            "room_type": self.room_type,
            "price_per_night": self.price_per_night,
            "is_booked": self.is_booked
        }


class Booking:
    def __init__(
        self,
        booking_id,
        customer_name,
        phone,
        room_number,
        room_type,
        check_in_date,
        nights,
        total_bill,
        status="Booked"
    ):
        self.booking_id = booking_id
        self.customer_name = customer_name
        self.phone = phone
        self.room_number = room_number
        self.room_type = room_type
        self.check_in_date = check_in_date
        self.nights = nights
        self.total_bill = total_bill
        self.status = status

    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "customer_name": self.customer_name,
            "phone": self.phone,
            "room_number": self.room_number,
            "room_type": self.room_type,
            "check_in_date": self.check_in_date,
            "nights": self.nights,
            "total_bill": self.total_bill,
            "status": self.status
        }


class HotelManagementSystem:
    def __init__(self):
        self.rooms_file = "rooms.json"
        self.bookings_file = "bookings.json"

        self.rooms = []
        self.bookings = []

        self.load_rooms()
        self.load_bookings()

    # ---------------- ROOM MANAGEMENT ---------------- #

    def load_rooms(self):
        if os.path.exists(self.rooms_file):
            with open(self.rooms_file, "r") as file:
                data = json.load(file)

            for room in data:
                new_room = Room(
                    room["room_number"],
                    room["room_type"],
                    room["price_per_night"]
                )
                new_room.is_booked = room["is_booked"]
                self.rooms.append(new_room)

        else:
            self.create_default_rooms()

    def create_default_rooms(self):
        default_rooms = [
            Room("101", "Standard", 1200),
            Room("102", "Standard", 1200),
            Room("103", "Standard", 1200),
            Room("201", "Deluxe", 2200),
            Room("202", "Deluxe", 2200),
            Room("301", "Suite", 4000),
            Room("302", "Suite", 4000)
        ]

        self.rooms = default_rooms
        self.save_rooms()

    def save_rooms(self):
        with open(self.rooms_file, "w") as file:
            json.dump(
                [room.to_dict() for room in self.rooms],
                file,
                indent=4
            )

    # ---------------- BOOKING MANAGEMENT ---------------- #

    def load_bookings(self):
        if os.path.exists(self.bookings_file):
            with open(self.bookings_file, "r") as file:
                data = json.load(file)

            self.bookings = [
                Booking(**booking)
                for booking in data
            ]

    def save_bookings(self):
        with open(self.bookings_file, "w") as file:
            json.dump(
                [booking.to_dict() for booking in self.bookings],
                file,
                indent=4
            )

    # ---------------- VIEW ROOMS ---------------- #

    def view_available_rooms(self):
        print("\n========== AVAILABLE ROOMS ==========")

        available = False

        for room in self.rooms:
            if not room.is_booked:
                available = True

                print(
                    f"Room: {room.room_number} | "
                    f"Type: {room.room_type} | "
                    f"Price: ₹{room.price_per_night}/night"
                )

        if not available:
            print("No rooms available.")

    # ---------------- BOOK ROOM ---------------- #

    def book_room(self):
        print("\n========== BOOK ROOM ==========")

        customer_name = input("Customer Name: ").strip()
        phone = input("Phone Number: ").strip()

        self.view_available_rooms()

        room_number = input(
            "\nEnter Room Number to Book: "
        ).strip()

        selected_room = None

        for room in self.rooms:
            if (
                room.room_number == room_number
                and not room.is_booked
            ):
                selected_room = room
                break

        if selected_room is None:
            print("Invalid or unavailable room.")
            return

        try:
            nights = int(
                input("Number of Nights: ")
            )

            if nights <= 0:
                print("Invalid number of nights.")
                return

        except ValueError:
            print("Invalid input.")
            return

        booking_id = (
            "BK"
            + str(len(self.bookings) + 1).zfill(4)
        )

        check_in_date = str(
            datetime.now().date()
        )

        total_bill = (
            selected_room.price_per_night * nights
        )

        booking = Booking(
            booking_id,
            customer_name,
            phone,
            selected_room.room_number,
            selected_room.room_type,
            check_in_date,
            nights,
            total_bill
        )

        self.bookings.append(booking)

        selected_room.is_booked = True

        self.save_bookings()
        self.save_rooms()

        print("\nRoom booked successfully!")
        print(f"Booking ID: {booking_id}")
        print(f"Total Bill: ₹{total_bill}")

    # ---------------- SEARCH BOOKING ---------------- #

    def search_booking(self):
        print("\n========== SEARCH BOOKING ==========")

        booking_id = input(
            "Enter Booking ID: "
        ).strip()

        for booking in self.bookings:

            if booking.booking_id == booking_id:

                print("\nBooking Found")
                print("-" * 35)

                print(
                    f"Booking ID : {booking.booking_id}"
                )
                print(
                    f"Customer   : {booking.customer_name}"
                )
                print(
                    f"Phone      : {booking.phone}"
                )
                print(
                    f"Room       : {booking.room_number}"
                )
                print(
                    f"Type       : {booking.room_type}"
                )
                print(
                    f"Check-In   : {booking.check_in_date}"
                )
                print(
                    f"Nights     : {booking.nights}"
                )
                print(
                    f"Bill       : ₹{booking.total_bill}"
                )
                print(
                    f"Status     : {booking.status}"
                )

                return

        print("Booking not found.")

    # ---------------- CHECK-IN ---------------- #

    def check_in(self):
        print("\n========== CHECK-IN ==========")

        booking_id = input(
            "Enter Booking ID: "
        ).strip()

        for booking in self.bookings:

            if booking.booking_id == booking_id:

                booking.status = "Checked-In"

                self.save_bookings()

                print(
                    "Customer checked in successfully."
                )

                return

        print("Booking not found.")

    # ---------------- CHECK-OUT ---------------- #

    def check_out(self):
        print("\n========== CHECK-OUT ==========")

        booking_id = input(
            "Enter Booking ID: "
        ).strip()

        for booking in self.bookings:

            if booking.booking_id == booking_id:

                booking.status = "Checked-Out"

                for room in self.rooms:

                    if (
                        room.room_number
                        == booking.room_number
                    ):
                        room.is_booked = False

                self.save_bookings()
                self.save_rooms()

                print(
                    "Customer checked out successfully."
                )

                return

        print("Booking not found.")

    # ---------------- CANCEL BOOKING ---------------- #

    def cancel_booking(self):
        print("\n========== CANCEL BOOKING ==========")

        booking_id = input(
            "Enter Booking ID: "
        ).strip()

        for booking in self.bookings:

            if booking.booking_id == booking_id:

                for room in self.rooms:

                    if (
                        room.room_number
                        == booking.room_number
                    ):
                        room.is_booked = False

                self.bookings.remove(booking)

                self.save_bookings()
                self.save_rooms()

                print(
                    "Booking cancelled successfully."
                )

                return

        print("Booking not found.")

    # ---------------- BILL GENERATION ---------------- #

    def generate_bill(self):
        print("\n========== BILL ==========")

        booking_id = input(
            "Enter Booking ID: "
        ).strip()

        for booking in self.bookings:

            if booking.booking_id == booking_id:

                print("\n" + "=" * 40)
                print("         HOTEL INVOICE")
                print("=" * 40)

                print(
                    f"Booking ID : {booking.booking_id}"
                )
                print(
                    f"Customer   : {booking.customer_name}"
                )
                print(
                    f"Room No    : {booking.room_number}"
                )
                print(
                    f"Room Type  : {booking.room_type}"
                )
                print(
                    f"Nights     : {booking.nights}"
                )

                print("-" * 40)

                print(
                    f"Total Bill : ₹{booking.total_bill}"
                )

                print("=" * 40)

                return

        print("Booking not found.")

    # ---------------- BOOKING HISTORY ---------------- #

    def booking_history(self):
        print("\n========== BOOKING HISTORY ==========")

        if not self.bookings:
            print("No bookings found.")
            return

        for booking in self.bookings:

            print("-" * 60)

            print(
                f"ID      : {booking.booking_id}"
            )

            print(
                f"Name    : {booking.customer_name}"
            )

            print(
                f"Room    : {booking.room_number}"
            )

            print(
                f"Bill    : ₹{booking.total_bill}"
            )

            print(
                f"Status  : {booking.status}"
            )

    # ---------------- DASHBOARD ---------------- #

    def dashboard(self):
        total_rooms = len(self.rooms)

        booked_rooms = len(
            [r for r in self.rooms if r.is_booked]
        )

        available_rooms = (
            total_rooms - booked_rooms
        )

        print("\n========== DASHBOARD ==========")

        print(f"Total Rooms      : {total_rooms}")
        print(f"Booked Rooms     : {booked_rooms}")
        print(
            f"Available Rooms  : {available_rooms}"
        )

        print(
            f"Total Bookings   : {len(self.bookings)}"
        )

    # ---------------- MENU ---------------- #

    def menu(self):
        while True:

            print("\n")
            print("=" * 50)
            print("     HOTEL ROOM BOOKING SYSTEM")
            print("=" * 50)

            print("1. View Available Rooms")
            print("2. Book Room")
            print("3. Search Booking")
            print("4. Check-In")
            print("5. Check-Out")
            print("6. Cancel Booking")
            print("7. Generate Bill")
            print("8. Booking History")
            print("9. Dashboard")
            print("0. Exit")

            print("=" * 50)

            choice = input(
                "Enter your choice: "
            ).strip()

            if choice == "1":
                self.view_available_rooms()

            elif choice == "2":
                self.book_room()

            elif choice == "3":
                self.search_booking()

            elif choice == "4":
                self.check_in()

            elif choice == "5":
                self.check_out()

            elif choice == "6":
                self.cancel_booking()

            elif choice == "7":
                self.generate_bill()

            elif choice == "8":
                self.booking_history()

            elif choice == "9":
                self.dashboard()

            elif choice == "0":
                print(
                    "Thank you for using the system!"
                )
                break

            else:
                print(
                    "Invalid choice. Try again."
                )


if __name__ == "__main__":
    hotel = HotelManagementSystem()
    hotel.menu()