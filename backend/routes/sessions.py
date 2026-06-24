from flask import Blueprint,request

from database import SessionLocal
from models import MealSession

sessions_bp = Blueprint(
    "sessions",
    __name__
)

@sessions_bp.route("/meal-session", methods=["POST"])
def create_meal_session():

    data = request.get_json()

    session = MealSession(
    name=data.get("name"),
    start_time=data.get("start_time"),
    end_time=data.get("end_time"),
    preorder_cutoff=data.get("preorder_cutoff"),
)
    db = SessionLocal()
    if db.query(MealSession).filter(
        MealSession.name == session.name
    ).first():
        return {
            "success": False,
            "message": "Meal session already exists"
        }, 400

    db.add(session)
    db.commit()

    return {
        "success": True,
        "message": "Meal session created"
    }

@sessions_bp.route("/meal-session", methods=["GET"])
def get_meal_sessions():

    db = SessionLocal()

    sessions = db.query(MealSession).all()

    result = []

    for session in sessions:

        result.append({
            "session_id": session.session_id,
            "name": session.name,
            "start_time": session.start_time,
            "end_time": session.end_time,
            "preorder_cutoff": session.preorder_cutoff,
            "active": session.active
        })

    return result