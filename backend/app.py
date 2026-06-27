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
from routes.orders import orders_bp

Base.metadata.create_all(bind=engine)
app = Flask(__name__)
CORS(app)    

app.register_blueprint(sessions_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(orders_bp)
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



if __name__ == "__main__":
    app.run(
        debug=True
    )