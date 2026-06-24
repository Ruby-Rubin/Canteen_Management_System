from flask import Blueprint,request
from database import SessionLocal
from models import MenuItem
menu_bp = Blueprint(
    "menu", __name__
)

@menu_bp.route("/menu", methods=["GET"])
def get_menu():

    db = SessionLocal()

    items = db.query(MenuItem).all()

    menu = []

    for item in items:
        menu.append({
            "menu_item_id": item.menu_item_id,
            "name": item.name,
            "price": float(item.price),
            "category": item.category,
            "available": item.available,
            "image_url": item.image_url
        })

    return menu

@menu_bp.route("/menu", methods=["POST"])
def create_menu_item():

    data = request.get_json()
    db= SessionLocal()

    if db.query(MenuItem).filter(MenuItem.name == data.get("name")).first() and db.query(MenuItem).filter(MenuItem.category == data.get("category")).first():
        return {
            "success": False,
            "message": "Menu item already exists"
        }, 400

    menu_item = MenuItem(
        name=data.get("name"),
        price=data.get("price"),
        category=data.get("category"),
        image_url=data.get("image_url")
    )

    db = SessionLocal()

    db.add(menu_item)
    db.commit()

    return {
        "success": True,
        "message": "Menu item created"
    }
