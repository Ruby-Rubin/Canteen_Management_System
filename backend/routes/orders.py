from flask import Blueprint, request
from database import SessionLocal
from models import Order, OrderItem, User, Cart, CartItem, MealSession, MenuItem

orders_bp = Blueprint("orders", __name__)

VALID_TRANSITIONS = {
    "PENDING": "PREPARING",
    "PREPARING": "READY",
    "READY": "COMPLETED"
}

prefix_map = {
    "Breakfast": "B",
    "Lunch": "L",
    "Snacks": "S",
    "Dinner": "D"
}
def serialize_order_summary(order, db):

    student = db.query(User).filter(
        User.user_id == order.student_id
    ).first()

    meal_session = db.query(MealSession).filter(
        MealSession.session_id == order.meal_session_id
    ).first()

    return {
        "order_id": order.order_id,
        "student_name": student.name,
        "register_no": student.register_no,
        "meal_session": meal_session.name,
        "token_number": order.token_number,
        "status": order.status,
        "order_type": order.order_type,
        "payment_method": order.payment_method,
        "total_amount": float(order.total_amount)
    }

@orders_bp.route("/orders", methods=["GET"])
def get_orders():
    db = SessionLocal()
    orders = db.query(Order).all()
    result = []
    for order in orders:
        result.append(
        serialize_order_summary(order, db)
    )
    db.close()
    return result 

@orders_bp.route("/orders/live", methods=["GET"])
def get_live_orders(): 
    db = SessionLocal()
    active_session = db.query(MealSession).filter(
    MealSession.active == True
).first()
    if not active_session:
        db.close()
        return {
        "success": False,
        "message": "No active meal session"
    }, 404
    orders = db.query(Order).filter(
    Order.meal_session_id == active_session.session_id
).all()
    result = []
    for order in orders:
        result.append(
        serialize_order_summary(order, db)
    )
    db.close()
    return result

@orders_bp.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    db = SessionLocal()
    order = db.query(Order).filter(
    Order.order_id == order_id
).first()
    if not order:
        db.close()
        return {
            "success": False,
            "message": "Order not found"
        }, 404
    student = db.query(User).filter(
    User.user_id == order.student_id).first()
    
    meal_session = db.query(MealSession).filter(
    MealSession.session_id == order.meal_session_id
).first()
    order_items = db.query(OrderItem).filter(
    OrderItem.order_id == order.order_id
).all()
    items = []
    for item in order_items:
        menu_item = db.query(MenuItem).filter(
    MenuItem.menu_item_id == item.menu_item_id
).first()
        items.append({
    "menu_item_id": menu_item.menu_item_id,
    "name": menu_item.name,
    "quantity": item.quantity,
    "price": float(item.price_at_purchase),
    "subtotal": float(item.price_at_purchase) * item.quantity
})
    db.close()
    return {
    "order_id": order.order_id,
    "student_name": student.name,
    "register_no": student.register_no,
    "meal_session": meal_session.name,
    "token_number": order.token_number,
    "status": order.status,
    "order_type": order.order_type,
    "payment_method": order.payment_method,
    "items": items,
    "total_amount": float(order.total_amount)
}

@orders_bp.route("/orders/<int:order_id>/status", methods=["PUT"])
def update_order_status(order_id):
    data = request.get_json()
    new_status = data.get("status")

    db = SessionLocal()

    order = db.query(Order).filter(
        Order.order_id == order_id
    ).first()

    if not order:
        db.close()
        return {
            "success": False,
            "message": "Order not found"
        }, 404

    current_status = order.status

    if current_status not in VALID_TRANSITIONS or VALID_TRANSITIONS[current_status] != new_status:
        db.close()
        return{
    "success": False,
    "message": f"Invalid status transition from {current_status} to {new_status}"
}, 400
    order.status = new_status
    db.commit()
    db.close()

    return {
        "success": True,
        "message": f"Order status updated to {new_status}"
    }
@orders_bp.route("/checkout", methods=["POST"])
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
        db.close()
        return {
            "success": False,
            "message": "Student not found"
        }, 404
    
    if student.role != "student":
        db.close()
        return {
        "success": False,
        "message": "Only students can place orders"
    }, 403

    session = db.query(MealSession).filter(
        MealSession.session_id == meal_session_id
    ).first()

    if not session:
        db.close()
        return {
            "success": False,
            "message": "Meal session not found"
        }, 404
    cart = db.query(Cart).filter(
        Cart.student_id == student_id,
        Cart.meal_session_id == meal_session_id
    ).first()

    if not cart:
        db.close()
        return {
            "success": False,
            "message": "Cart not found"
        }, 404
    cart_items = db.query(CartItem).filter(
        CartItem.cart_id == cart.cart_id
    ).all()

    if not cart_items:
        db.close()
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
    if session.active:
        order_type = "LIVE"
    else:
        order_type = "PREORDER"
    order = Order(
    student_id=student_id,
    meal_session_id=meal_session_id,
    token_number=token_number,
    order_type=order_type,
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
    db.close()
    return {
    "success": True,
    "order_id": order.order_id,
    "token_number": token_number,
    "total_amount": total_amount
}

@orders_bp.route("/orders/preorders", methods=["GET"])
def get_preorders():

    db = SessionLocal()

    active_session = db.query(MealSession).filter(
    MealSession.active == True
).first()
    if not active_session:
        db.close()
        return {
        "success": False,
        "message": "No active meal session"
    }, 404
    future_sessions=db.query(MealSession).filter(
        MealSession.display_order > active_session.display_order
    ).all()
    if not future_sessions:
        db.close()
        return [] 
    future_session_ids=[]
    for session in future_sessions:
        future_session_ids.append(session.session_id)
    orders = db.query(Order).filter(
    Order.meal_session_id.in_(future_session_ids)
).all()
    result = []
    for order in orders:
        result.append(
        serialize_order_summary(order, db)
    )
    db.close()
    return result
