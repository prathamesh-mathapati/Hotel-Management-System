import json
import os

DATA_FILE = "hotel_data.json"

default_rooms = {
    "101": {"type": "Single", "price": 1000, "booked": False},
    "102": {"type": "Single", "price": 1000, "booked": False},
    "201": {"type": "Double", "price": 2000, "booked": False},
    "202": {"type": "Double", "price": 2000, "booked": False},
    "301": {"type": "Suite", "price": 4000, "booked": False},
}

data = {
    "rooms": default_rooms,
    "customers": {}
}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_data():
    global data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

load_data()

def view_rooms():
    print("\n--- Room Status ---")
    print(f"{'Room':<6} | {'Type':<8} | {'Price':<6} | {'Status'}")
    print("-" * 35)
    for room_no, info in data["rooms"].items():
        status = "Booked 🔴" if info["booked"] else "Available 🟢"
        print(f"{room_no:<6} | {info['type']:<8} | ₹{info['price']:<5} | {status}")

def book_room():
    name = input("Enter customer name: ")
    room_no = input("Enter room number: ") # Keep as string for JSON keys

    if room_no not in data["rooms"]:
        print("Invalid Room Number!")
        return

    if data["rooms"][room_no]["booked"]:
        print("Room already booked!")
        return

    try:
        days = int(input("Number of days: "))
    except ValueError:
        print("Please enter a valid number for days.")
        return

    cost = data["rooms"][room_no]["price"] * days
    
    data["rooms"][room_no]["booked"] = True
    data["customers"][name] = {
        "room": room_no,
        "days": days,
        "bill": cost
    }

    save_data()
    print(f"Room booked successfully! Total Bill: ₹{cost}")

def checkout():
    name = input("Enter customer name: ")

    if name not in data["customers"]:
        print("Customer not found!")
        return

    info = data["customers"][name]
    room_no = info["room"]

    print("\n----- 🧾 BILL -----")
    print(f"Name: {name}")
    print(f"Room: {room_no}")
    print(f"Days: {info['days']}")
    print(f"Total: ₹{info['bill']}")
    print("-------------------")

    if room_no in data["rooms"]:
        data["rooms"][room_no]["booked"] = False
    
    del data["customers"][name]
    save_data()
    print("Checked out successfully!")

while True:
    print("\n🏨 --- HOTEL MANAGEMENT SYSTEM ---")
    print("1. View Rooms")
    print("2. Book Room")
    print("3. Check-Out")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        view_rooms()
    elif choice == "2":
        view_rooms() 
        book_room()
    elif choice == "3":
        checkout()
    elif choice == "4":
        print("Goodbye! 👋")
        break
    else:
        print("Invalid choice, please try again.")