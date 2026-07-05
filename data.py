import json
import os

JSON_FILE = "seats.json"

TOTAL_ROWS = 80
SEAT_COLUMNS = ["A", "B", "C", "D", "E", "F"]
STORAGE_ROWS = {77, 78}
STORAGE_COLUMNS = {"D", "E", "F"}


def load():
    """
    Loads seat data from JSON. If no file exists yet,
    builds a fresh seat map, saves it, and returns it.
    """
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            return json.load(f)

    # First run - build and save a fresh seat map
    print("First run - creating fresh seat map...")
    seats = {}
    for row in range(1, TOTAL_ROWS + 1):
        for col in SEAT_COLUMNS:
            seat_id = f"{row}{col}"
            if row in STORAGE_ROWS and col in STORAGE_COLUMNS:
                seats[seat_id] = "S"
            else:
                seats[seat_id] = "F"
    save(seats)
    return seats


def save(seats):
    """Saves the current seat map to JSON."""
    with open(JSON_FILE, "w") as f:
        json.dump(seats, f, indent=2)
