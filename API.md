Authentication
--------------
POST /login
POST /change-password

Users
-----
GET /users
POST /users
PUT /users/<id>

Sessions
--------
GET /sessions
POST /sessions

Menu
----
GET /menu
POST /menu

Cart
----
POST /cart/add
GET /cart/<student_id>/<meal_session_id>
DELETE /cart/item/<id>

Orders
------
POST /checkout
GET /orders
GET /orders/<id>
GET /orders/live
GET /orders/preorders
PUT /orders/<id>/status