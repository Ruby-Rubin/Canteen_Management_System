from werkzeug.security import generate_password_hash

from database import SessionLocal
from models import User, MealSession, MenuItem

db = SessionLocal()

existing_user = db.query(User).filter(
    User.email == "rubin@mail.com"
).first()

if not existing_user:

    student = User(
        name="Rubin",
        email="rubin@mail.com",
        register_no="23ADS101",
        password_hash=generate_password_hash("rr"),
        role="student",
        active=True,
        must_change_password=False
    )

    db.add(student)
    print("Student created")

else:
    print("Student already exists")

meal_sessions = [
    {
        "name": "Breakfast",
        "display_order": 1,
        "start_time": "07:30",
        "end_time": "09:30",
        "preorder_cutoff": "07:00",
        "active": False
    },
    {
        "name": "Lunch",
        "display_order": 2,
        "start_time": "12:00",
        "end_time": "14:00",
        "preorder_cutoff": "11:30",
        "active": True
    },
    {
        "name": "Snacks",
        "display_order": 3,
        "start_time": "16:00",
        "end_time": "17:30",
        "preorder_cutoff": "15:30",
        "active": False
    },
    {
        "name": "Dinner",
        "display_order": 4,
        "start_time": "19:00",
        "end_time": "21:00",
        "preorder_cutoff": "18:30",
        "active": False
    }
]

for session in meal_sessions:

    existing = db.query(MealSession).filter(
        MealSession.name == session["name"]
    ).first()

    if existing:
        print(f"{session['name']} already exists")
        continue

    new_session = MealSession(
        name=session["name"],
        display_order=session["display_order"],
        start_time=session["start_time"],
        end_time=session["end_time"],
        preorder_cutoff=session["preorder_cutoff"],
        active=session["active"]
    )

    db.add(new_session)

    print(f"{session['name']} created")
menu_items = [
    {
        "name": "Chicken Rice",
        "price": 80,
        "category": "Lunch"
    },
    {
        "name": "Veg Meals",
        "price": 70,
        "category": "Lunch"
    },
    {
        "name": "Masala Dosa",
        "price": 50,
        "category": "Breakfast"
    },
    {
        "name": "Coffee",
        "price": 20,
        "category": "Breakfast"
    }
]
for item in menu_items:

    existing = db.query(MenuItem).filter(
        MenuItem.name == item["name"]
    ).first()

    if existing:
        print(f"{item['name']} already exists")
        continue

    menu = MenuItem(
        name=item["name"],
        price=item["price"],
        category=item["category"],
        available=True
    )

    db.add(menu)

    print(f"{item['name']} created")

db.commit()
db.close()

print("Seed data completed.")