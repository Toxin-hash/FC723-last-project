import random
import sqlite3
import string
import data

WINDOW_COLUMNS = {"A", "F"}
AISLE_COLUMNS = {"C", "D"}

REFERENCE_ALPHABET = string.ascii_uppercase + string.digits
REFERENCE_LENGTH = 8

DB_FILE = "passengers.db"

def generate_reference(existing_refs):
    """Generate a random unique 8-character alphanumeric booking reference."""
    existing_refs = set(existing_refs)
    while True:
        candidate = "".join(random.choice(REFERENCE_ALPHABET) for _ in range(REFERENCE_LENGTH))
        if candidate not in existing_refs:
            return candidate


def _connect():
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS passengers (
            booking_ref TEXT PRIMARY KEY, passport TEXT NOT NULL,
            first_name TEXT NOT NULL, last_name TEXT NOT NULL,
            seat_row INTEGER NOT NULL, seat_col TEXT NOT NULL)"""
    )
    return conn


def _get_existing_references():
    with _connect() as conn:
        return {r[0] for r in conn.execute("SELECT booking_ref FROM passengers")}


def _add_passenger(ref, passport, first, last, row, col):
    with _connect() as conn:
        conn.execute(
            "INSERT INTO passengers VALUES (?, ?, ?, ?, ?, ?)",
            (ref, passport, first, last, row, col),
        )


def _remove_passenger(ref):
    with _connect() as conn:
        conn.execute("DELETE FROM passengers WHERE booking_ref = ?", (ref,))

def is_booked(status):
    return status not in ("F", "S")

def check(seats, seat_id):
    """Check and print the status of a seat."""
    if seat_id not in seats:
        print(f"'{seat_id}' is not a valid seat.")
        return
    status = seats[seat_id]
    if status == "F":
        print(f"Seat {seat_id} is FREE.")
    elif status == "S":
        print(f"Seat {seat_id} is a STORAGE area - cannot be booked.")
    else:
        print(f"Seat {seat_id} is BOOKED (reference: {status}).")


def book(seats, seat_id):
    """Book a seat if it exists and is free. Saves to JSON and DB after."""
    if seat_id not in seats:
        print(f"'{seat_id}' is not a valid seat.")
        return
    if seats[seat_id] == "S":
        print(f"Seat {seat_id} is storage - cannot be booked.")
        return
    if is_booked(seats[seat_id]):
        print(f"Seat {seat_id} is already booked (reference: {seats[seat_id]}).")
        return

    passport = input("Enter passport number: ").strip()
    first_name = input("Enter first name: ").strip()
    last_name = input("Enter last name: ").strip()

    booking_ref = generate_reference(_get_existing_references())
    row, col = int(seat_id[:-1]), seat_id[-1]
    _add_passenger(booking_ref, passport, first_name, last_name, row, col)

    seats[seat_id] = booking_ref
    data.save(seats)
    print(f"Seat {seat_id} booked successfully. Booking reference: {booking_ref}")


def free(seats, seat_id):
    """Free a seat if it exists and is booked. Saves to JSON and DB after."""
    if seat_id not in seats:
        print(f"'{seat_id}' is not a valid seat.")
        return
    status = seats[seat_id]
    if status == "F":
        print(f"Seat {seat_id} is already free.")
        return
    if status == "S":
        print(f"Seat {seat_id} is storage - cannot be freed.")
        return

    _remove_passenger(status)
    seats[seat_id] = "F"
    data.save(seats)
    print(f"Seat {seat_id} has been freed.")


def status(seats):
    """Print the full seat map grid and summary counts."""
    print("\n--- Burak757 Seating Chart ---")
    print("(F = Free, R = Reserved, S = Storage)\n")
    for row in range(1, 81):
        row_cells = []
        for col in ["A", "B", "C", "D", "E", "F"]:
            seat_id = f"{row}{col}"
            display_value = "R" if is_booked(seats[seat_id]) else seats[seat_id]
            row_cells.append(f"{col}:{display_value}")
            if col == "C":
                row_cells.append("|")
        print(f"Row {row:>2}: " + " ".join(row_cells))

    free_count = sum(1 for v in seats.values() if v == "F")
    storage_count = sum(1 for v in seats.values() if v == "S")
    booked_count = sum(1 for v in seats.values() if is_booked(v))
    print(f"\nSummary: {free_count} free | {booked_count} booked | {storage_count} storage\n")


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