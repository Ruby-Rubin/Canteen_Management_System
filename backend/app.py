from flask import Flask
from flask_cors import CORS
from flask import request
from werkzeug.security import check_password_hash, generate_password_hash
from database import SessionLocal,engine 
from models import User,MenuItem,Base,MealSession,CartItem,Cart,Order,OrderItem 
from routes.sessions import sessions_bp
from routes.menu import menu_bp
from routes.users import users_bp
from routes.auth import auth_bp
from routes.cart import cart_bp

Base.metadata.create_all(bind=engine)
app = Flask(__name__)
CORS(app)    
prefix_map = {
    "Breakfast": "B",
    "Lunch": "L",
    "Snacks": "S",
    "Dinner": "D"
}
app.register_blueprint(sessions_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(cart_bp)
@app.route("/")
def home():
    return {
        "message": "College Canteen API Running"
    }





@app.route("/admin/dashboard")
def admin_dashboard():

    role = request.args.get("role")

    if role != "admin":
        return {
            "success": False,
            "message": "Access Denied"
        }, 403

    return {
        "success": True,
        "message": "Welcome Admin"
    }






@app.route("/checkout", methods=["POST"])
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

if __name__ == "__main__":
    app.run(
        debug=True
    )