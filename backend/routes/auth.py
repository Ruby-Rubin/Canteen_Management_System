from flask import Blueprint, request
from database import SessionLocal
from models import User
from werkzeug.security import generate_password_hash,check_password_hash

auth_bp = Blueprint(
    "auth", __name__
)

@auth_bp.route("/login",methods=["POST"])
def login():

    data = request.get_json()

    register_no = data.get("register_no")
    password = data.get("password")

    db = SessionLocal()

    user = db.query(User).filter(
        User.register_no==register_no,
    ).first()

    if not user:
        return {
            "success": False,
            "message": "User not found"
        }, 404

    if not user.active:
        return {
        "success": False,
        "message": "Account is disabled"
    }, 403

    if not check_password_hash(
        user.password_hash,
        password
    ):
        return {
            "success": False,
            "message": "Invalid password"
            
        }, 401

    return {
    "success": True,
    "user_id": user.user_id,
    "name": user.name,
    "email": user.email,
    "register_no": user.register_no,
    "role": user.role,
    "must_change_password": user.must_change_password
}

@auth_bp.route("/change-password", methods=["PUT"])
def change_password():

    data = request.get_json()

    user_id = data.get("user_id")
    new_password = data.get("new_password")

    db = SessionLocal()

    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if not user:
        return {
            "success": False,
            "message": "User not found"
        }, 404

    user.password_hash = generate_password_hash(
        new_password
    )

    user.must_change_password = False

    db.commit()

    return {
        "success": True,
        "message": "Password updated successfully",
        "email": user.email,
        "register_no": user.register_no
    }