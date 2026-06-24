from database import SessionLocal
from models import User

db = SessionLocal()

users = db.query(User).all()

for user in users:
    print(
        user.user_id,
        user.name,
        user.email,
        user.role,
        user.register_no,
        user.must_change_password
    )