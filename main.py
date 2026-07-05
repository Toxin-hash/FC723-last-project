import booking_ops
import data


def menu():
    seats = data.load()

    while True:
        print("\n===== Apache Airlines - Seat Booking System =====")
        print("1. Check availability of seat")
        print("2. Book a seat")
        print("3. Free a seat")
        print("4. Show booking status")
        print("5. Find seats by preference (window/aisle)")
        print("6. Exit program")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            seat_id = input("Enter seat ID (e.g. 12A): ").strip().upper()
            booking_ops.check(seats, seat_id)
        elif choice == "2":
            seat_id = input("Enter seat ID to book (e.g. 12A): ").strip().upper()
            booking_ops.book(seats, seat_id)
        elif choice == "3":
            seat_id = input("Enter seat ID to free (e.g. 12A): ").strip().upper()
            booking_ops.free(seats, seat_id)
        elif choice == "4":
            booking_ops.status(seats)
        elif choice == "5":
            booking_ops.find_by_preference(seats)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option, please choose 1-6.")


if __name__ == "__main__":
    menu()
