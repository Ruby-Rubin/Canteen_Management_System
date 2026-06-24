from werkzeug.security import generate_password_hash

from database import SessionLocal
from models import User


db = SessionLocal()

existing_admin = db.query(User).filter(
    User.email == "admin@canteen.com"
).first()

if existing_admin:
    print("Admin already exists")

else:
    admin = User(
        name="Admin",
        email="admin@canteen.com",
        register_no="ADMIN001",
        password_hash=generate_password_hash("admin123"),
        role="admin",
        active=True,
        must_change_password=False
    )

    db.add(admin)
    db.commit()

    print("Admin account created")