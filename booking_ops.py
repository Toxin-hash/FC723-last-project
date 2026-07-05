import data

WINDOW_COLUMNS = {"A", "F"}
AISLE_COLUMNS = {"C", "D"}


def check(seats, seat_id):
    """Check and print the status of a seat."""
    if seat_id not in seats:
        print(f"'{seat_id}' is not a valid seat.")
        return
    status = seats[seat_id]
    if status == "F":
        print(f"Seat {seat_id} is FREE.")
    elif status == "R":
        print(f"Seat {seat_id} is BOOKED.")
    elif status == "S":
        print(f"Seat {seat_id} is a STORAGE area - cannot be booked.")


def book(seats, seat_id):
    """Book a seat if it exists and is free. Saves to JSON after."""
    if seat_id not in seats:
        print(f"'{seat_id}' is not a valid seat.")
        return
    if seats[seat_id] == "F":
        seats[seat_id] = "R"
        data.save(seats)
        print(f"Seat {seat_id} booked successfully.")
    elif seats[seat_id] == "R":
        print(f"Seat {seat_id} is already booked.")
    elif seats[seat_id] == "S":
        print(f"Seat {seat_id} is storage - cannot be booked.")


def free(seats, seat_id):
    """Free a seat if it exists and is booked. Saves to JSON after."""
    if seat_id not in seats:
        print(f"'{seat_id}' is not a valid seat.")
        return
    if seats[seat_id] == "R":
        seats[seat_id] = "F"
        data.save(seats)
        print(f"Seat {seat_id} has been freed.")
    elif seats[seat_id] == "F":
        print(f"Seat {seat_id} is already free.")
    elif seats[seat_id] == "S":
        print(f"Seat {seat_id} is storage - cannot be freed.")


def status(seats):
    """Print the full seat map grid and summary counts."""
    print("\n--- Burak757 Seating Chart ---")
    print("(F = Free, R = Reserved, S = Storage)\n")
    for row in range(1, 81):
        row_cells = []
        for col in ["A", "B", "C", "D", "E", "F"]:
            seat_id = f"{row}{col}"
            row_cells.append(f"{col}:{seats[seat_id]}")
            if col == "C":
                row_cells.append("|")
        print(f"Row {row:>2}: " + " ".join(row_cells))
    print(f"\nSummary: {sum(1 for v in seats.values() if v == 'F')} free | "
          f"{sum(1 for v in seats.values() if v == 'R')} booked | "
          f"{sum(1 for v in seats.values() if v == 'S')} storage\n")


def find_by_preference(seats):
    """Find free seats by preference: window, aisle, or any."""
    print("\nPreference options: window / aisle / any")
    pref = input("Enter preference: ").strip().lower()
    if pref not in {"window", "aisle", "any"}:
        print("Please enter 'window', 'aisle', or 'any'.")
        return
    matches = []
    for seat_id, s in seats.items():
        if s != "F":
            continue
        col = seat_id[-1]
        if pref == "window" and col in WINDOW_COLUMNS:
            matches.append(seat_id)
        elif pref == "aisle" and col in AISLE_COLUMNS:
            matches.append(seat_id)
        elif pref == "any":
            matches.append(seat_id)
    matches = sorted(matches, key=lambda s: (int(s[:-1]), s[-1]))
    if not matches:
        print(f"No free seats found for '{pref}'.")
        return
    print(f"Found {len(matches)} free seat(s). Showing first 10: {matches[:10]}")
