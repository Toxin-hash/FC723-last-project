import booking_ops
import data


def display_map(seats, rows_per_page=20):
    symbols = {"F": ".", "S": "#"}  # free -> ".", storage -> "#"

    def cell_symbol(seat_id):
        val = seats[seat_id]
        if val in symbols:
            return symbols[val]
        return "X"  # booked

    header = "     A   B   C     D   E   F"
    divider = "   +---+---+---+   +---+---+---+"

    print("\n===== Apache Airlines / Burak757 - Seat Map Diagram =====")
    print("Legend:  .  = Free    X  = Booked    #  = Storage\n")

    total_rows = 80
    for start in range(1, total_rows + 1, rows_per_page):
        end = min(start + rows_per_page - 1, total_rows)
        print(header)
        print(divider)
        for row in range(start, end + 1):
            left = [cell_symbol(f"{row}{c}") for c in ["A", "B", "C"]]
            right = [cell_symbol(f"{row}{c}") for c in ["D", "E", "F"]]
            left_str = " | ".join(left)
            right_str = " | ".join(right)
            print(f"{row:>3}| {left_str} |   | {right_str} |")
            print(divider)

        free_count = sum(1 for r in range(start, end + 1) for c in "ABCDEF" if seats[f"{r}{c}"] == "F")
        booked_count = sum(1 for r in range(start, end + 1) for c in "ABCDEF" if booking_ops.is_booked(seats[f"{r}{c}"]))
        storage_count = sum(1 for r in range(start, end + 1) for c in "ABCDEF" if seats[f"{r}{c}"] == "S")
        print(f"Rows {start}-{end}: {free_count} free | {booked_count} booked | {storage_count} storage")

        if end < total_rows:
            input("\n-- Press Enter to see the next rows --\n")

    print("===== End of seat map =====\n")


def menu():
    seats = data.load()

    while True:
        print("\n===== Apache Airlines - Seat Booking System =====")
        print("1. Check availability of seat")
        print("2. Book a seat")
        print("3. Free a seat")
        print("4. Show booking status")
        print("5. Show seat map diagram")
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
            display_map(seats)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option, please choose 1-6.")


if __name__ == "__main__":
    menu()