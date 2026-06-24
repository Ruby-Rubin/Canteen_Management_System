from flask import Blueprint, request
from database import SessionLocal
from models import Order, OrderItem, User, Cart, CartItem, MealSession, MenuItem

cart_bp = Blueprint("cart", __name__)

prefix_map = {
    "Breakfast": "B",
    "Lunch": "L",
    "Snacks": "S",
    "Dinner": "D"
}

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

@cart_bp.route("/checkout", methods=["POST"])
def checkout():

    data = request.get_json()

    student_id = data.get("student_id")
    meal_session_id = data.get("meal_session_id")
    payment_method = data.get("payment_method")

    db = SessionLocal()
    
    student = db.query(User).filter(
        User.user_id == student_id
    ).first()

    if not student:
        return {
            "success": False,
            "message": "Student not found"
        }, 404
    
    if student.role != "student":
        return {
        "success": False,
        "message": "Only students can place orders"
    }, 403

    session = db.query(MealSession).filter(
        MealSession.session_id == meal_session_id
    ).first()

    if not session:
        return {
            "success": False,
            "message": "Meal session not found"
        }, 404
    cart = db.query(Cart).filter(
        Cart.student_id == student_id,
        Cart.meal_session_id == meal_session_id
    ).first()

    if not cart:
        return {
            "success": False,
            "message": "Cart not found"
        }, 404
    cart_items = db.query(CartItem).filter(
        CartItem.cart_id == cart.cart_id
    ).all()

    if not cart_items:
        return {
            "success": False,
            "message": "Cart is empty"
        }, 400
    total_amount = 0

    for item in cart_items:

        menu_item = db.query(MenuItem).filter(
            MenuItem.menu_item_id == item.menu_item_id
        ).first()

        total_amount += (
            float(menu_item.price)
            * item.quantity
        )
    order_count = db.query(Order).count() + 1

    prefix = prefix_map.get(
        session.name,
        "X"
    )

    token_number = f"{prefix}-{order_count}"
    order = Order(
        student_id=student_id,
        meal_session_id=meal_session_id,
        token_number=token_number,
        order_type="PREORDER",
        payment_method=payment_method,
        total_amount=total_amount
    )

    db.add(order)
    db.commit()
    for item in cart_items:

        menu_item = db.query(MenuItem).filter(
            MenuItem.menu_item_id == item.menu_item_id
        ).first()

        order_item = OrderItem(
            order_id=order.order_id,
            menu_item_id=item.menu_item_id,
            quantity=item.quantity,
            price_at_purchase=float(menu_item.price)
        )

        db.add(order_item)
    db.commit()
    for item in cart_items:
        db.delete(item)

    db.delete(cart)
    
    db.commit()
    return {
    "success": True,
    "order_id": order.order_id,
    "token_number": token_number,
    "total_amount": total_amount
}