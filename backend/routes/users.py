from flask import Blueprint, request
from database import SessionLocal
from models import   User
from werkzeug.security import generate_password_hash
users_bp = Blueprint(
    "users", __name__
)

@users_bp.route("/users", methods=["GET"])
def get_users():

    db = SessionLocal()

    users = db.query(User).all()

    result = []

    for user in users:

        result.append({
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "register_no": user.register_no,
            "role": user.role,
            "active": user.active,
            "must_change_password": user.must_change_password
        })

    return result

@users_bp.route("/users", methods=["POST"])
def create_user():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    register_no = data.get("register_no")
    role = data.get("role")
    dob = data.get("dob")

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:
        return {
            "success": False,
            "message": "Email already exists"
        }, 400

    user = User(
        name=name,
        email=email,
        register_no=register_no,
        role=role,
        password_hash=generate_password_hash(dob),
        must_change_password=True
    )

    db.add(user)
    db.commit()

    return {
        "success": True,
        "message": f"{role} account created"
    }

@users_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):

    data = request.get_json()

    db = SessionLocal()

    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if not user:
        return {
            "success": False,
            "message": "User not found"
        }, 404

    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    user.role = data.get("role", user.role)
    user.active = data.get("active", user.active)

    db.commit()

    return {
        "success": True,
        "message": "User updated successfully"
    }