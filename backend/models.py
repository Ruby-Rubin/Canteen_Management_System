from sqlalchemy import Column, Float, Float, Numeric
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from datetime import datetime

from database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    register_no = Column(String, unique=True)

    password_hash = Column(String, nullable=False)

    role = Column(String, nullable=False)

    active = Column(Boolean, default=True)

    must_change_password = Column(Boolean, default=True)

class MenuItem(Base):
    __tablename__ = "menu_items"

    menu_item_id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    price = Column(Numeric(10, 2), nullable=False)
    category = Column(String, nullable=False)



    available = Column(Boolean, default=True)
    image_url = Column(String)

class MealSession(Base):
    __tablename__ = "meal_sessions"

    session_id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    start_time = Column(String, nullable=False)

    end_time = Column(String, nullable=False)

    preorder_cutoff = Column(String, nullable=False)

    active = Column(Boolean, default=True)

class Cart(Base):
    __tablename__ = "carts"

    cart_id = Column(Integer, primary_key=True)

    student_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    meal_session_id = Column(
        Integer,
        ForeignKey("meal_sessions.session_id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class CartItem(Base):
    __tablename__ = "cart_items"

    cart_item_id = Column(
        Integer,
        primary_key=True
    )

    cart_id = Column(
        Integer,
        ForeignKey("carts.cart_id"),
        nullable=False
    )

    menu_item_id = Column(
        Integer,
        ForeignKey("menu_items.menu_item_id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=1
    )

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(
        Integer,
        primary_key=True
    )

    student_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    meal_session_id = Column(
        Integer,
        ForeignKey("meal_sessions.session_id"),
        nullable=False
    )

    token_number = Column(
        String,
        nullable=False
    )

    order_type = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        default="PENDING"
    )

    payment_method = Column(
        String
    )

    payment_status = Column(
        String,
        default="PENDING"
    )

    total_amount = Column(
        Float,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(
        Integer,
        primary_key=True
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.order_id"),
        nullable=False
    )

    menu_item_id = Column(
        Integer,
        ForeignKey("menu_items.menu_item_id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    price_at_purchase = Column(
        Float,
        nullable=False
    )