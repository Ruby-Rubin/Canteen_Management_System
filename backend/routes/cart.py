from flask import Blueprint, request
from database import SessionLocal
from models import User, Cart, CartItem, MealSession, MenuItem

cart_bp = Blueprint("cart", __name__)

@cart_bp.route("/cart/session/<int:student_id>/<int:meal_session_id>", methods=["GET"])
def get_session_cart(student_id, meal_session_id):

    db = SessionLocal()

    cart = db.query(Cart).filter(
        Cart.student_id == student_id,
        Cart.meal_session_id == meal_session_id
    ).first()       

    if not cart:
        return []

    cart_items = db.query(CartItem).filter(
        CartItem.cart_id == cart.cart_id
    ).all()

    result = []

    for cart_item in cart_items:

        menu_item = db.query(MenuItem).filter(
            MenuItem.menu_item_id == cart_item.menu_item_id
        ).first()

        result.append({
            "cart_item_id": cart_item.cart_item_id,
            "menu_item_id": menu_item.menu_item_id,
            "name": menu_item.name,
            "price": float(menu_item.price),
            "quantity": cart_item.quantity
        })

    return result


@cart_bp.route("/cart/add", methods=["POST"])
def add_to_cart():

    data = request.get_json()

    student_id = data.get("student_id")
    menu_item_id = data.get("menu_item_id")
    quantity = data.get("quantity", 1)
    meal_session_id = data.get("meal_session_id")

    db = SessionLocal()

    cart = db.query(Cart).filter(
    Cart.student_id == student_id,
    Cart.meal_session_id == meal_session_id
).first()
    student = db.query(User).filter(
    User.user_id == student_id
).first()   
    if not student:
        return {
        "success": False,
        "message": "Student not found"
    }, 404

    meal_session = db.query(MealSession).filter(
    MealSession.session_id == meal_session_id
).first()
    
    if not meal_session:
        return {
        "success": False,
        "message": "Meal session not found"
    }, 404

    if student.role != "student":
        return {
        "success": False,
        "message": "Only students can create carts"
    }, 403
    if not cart:

        cart = Cart(
            student_id=student_id,
            meal_session_id=meal_session_id
        )

        db.add(cart)
        db.commit()

    existing_item = db.query(CartItem).filter(
    CartItem.cart_id == cart.cart_id,
    CartItem.menu_item_id == menu_item_id
).first()
    if existing_item:
        existing_item.quantity += quantity
        db.commit()
        return {
        "success": True,
        "message": "Cart quantity updated"
    }
    cart_item = CartItem(
    cart_id=cart.cart_id,
    menu_item_id=menu_item_id,
    quantity=quantity
)
    db.add(cart_item)
    db.commit()

    return {
    "success": True,
    "message": "Item added to cart"
}

@cart_bp.route("/cart/item/<int:cart_item_id>", methods=["DELETE"])
def delete_cart_item(cart_item_id):

    db = SessionLocal()

    cart_item = db.query(CartItem).filter(  
        CartItem.cart_item_id == cart_item_id
    ).first()

    if not cart_item:
        return {
            "success": False,
            "message": "Cart item not found"
        }, 404

    db.delete(cart_item)
    db.commit()

    return {
        "success": True,
        "message": "Item removed from cart"
    }

@cart_bp.route("/cart/session", methods=["POST"])
def create_session_cart():

    data = request.get_json()

    student_id = data.get("student_id")
    meal_session_id = data.get("meal_session_id")

    db = SessionLocal()

    existing_cart = db.query(Cart).filter(
        Cart.student_id == student_id,
        Cart.meal_session_id == meal_session_id
    ).first()

    if existing_cart:
        return {
            "success": True,
            "message": "Cart already exists",
            "cart_id": existing_cart.cart_id
        }

    cart = Cart(
        student_id=student_id,
        meal_session_id=meal_session_id
    )

    db.add(cart)
    db.commit()

    return {
        "success": True,
        "message": "Cart created",
        "cart_id": cart.cart_id
    }

