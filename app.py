# from flask import Flask, request, jsonify
# from datetime import datetime
# import mysql.connector

# app = Flask(__name__)

# # Database connection
# def get_db_connection():
#     return mysql.connector.connect(
#         host='localhost',
#         user='root',
#         password='password',
#         database='sushi_shop'
#     )

# # Calculate discount
# def calculate_discount(quantity, order_time):
#     discount = 0
#     if quantity >= 20:
#         discount = 0.20
#     elif quantity >= 10:
#         discount = 0.10

#     if order_time.hour >= 11 and order_time.hour < 14:
#         discount += 0.20

#     return discount

# # Add to cart endpoint
# @app.route('/add_to_cart', methods=['POST'])
# def add_to_cart():
#     data = request.json
#     sushi_a_quantity = data.get('sushiA', 0)
#     sushi_b_quantity = data.get('sushiB', 0)
#     order_time = datetime.now()

#     sushi_a_price = 3 * sushi_a_quantity
#     sushi_b_price = 4 * sushi_b_quantity
#     total_price = sushi_a_price + sushi_b_price
#     total_quantity = sushi_a_quantity + sushi_b_quantity

#     discount_rate = calculate_discount(total_quantity, order_time)
#     discount_applied = total_price * discount_rate
#     final_price = total_price - discount_applied

#     connection = get_db_connection()
#     cursor = connection.cursor()

#     # Insert order into database
#     cursor.execute(
#         "INSERT INTO orders (total_price, discount_applied, final_price) VALUES (%s, %s, %s)",
#         (total_price, discount_applied, final_price)
#     )
#     order_id = cursor.lastrowid

#     # Insert order items into database
#     cursor.execute(
#         "INSERT INTO order_items (order_id, sushi_type, quantity, price) VALUES (%s, %s, %s, %s)",
#         (order_id, 'A', sushi_a_quantity, sushi_a_price)
#     )
#     cursor.execute(
#         "INSERT INTO order_items (order_id, sushi_type, quantity, price) VALUES (%s, %s, %s, %s)",
#         (order_id, 'B', sushi_b_quantity, sushi_b_price)
#     )

#     connection.commit()
#     cursor.close()
#     connection.close()

#     return jsonify({'message': 'Order added successfully', 'order_id': order_id})

# # Fetch orders endpoint
# @app.route('/fetch_orders', methods=['GET'])
# def fetch_orders():
#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)

#     cursor.execute("SELECT * FROM orders")
#     orders = cursor.fetchall()

#     for order in orders:
#         cursor.execute(
#             "SELECT sushi_type, quantity, price FROM order_items WHERE order_id = %s", 
#             (order['order_id'],)
#         )
#         order['items'] = cursor.fetchall()

#     cursor.close()
#     connection.close()

#     return jsonify(orders)

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, request, jsonify
from datetime import datetime
import mysql.connector

app = Flask(__name__)
from flask_cors import CORS
CORS(app)

# Database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='', # SQLDeRe001#
        database='sushi_shop'
    )
    return conn

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    print('+++++++++++++++++++++++++++++Entered add to cart++++++++++++++++++++++++++++++++++++++++')
    data = request.json
    sushiA = data.get('sushiA')
    sushiB = data.get('sushiB')
    
    if sushiA is None or sushiB is None:
        return jsonify({"message": "Invalid order data"}), 400
    
    total_before_discount = sushiA * 3 + sushiB * 4
    total_discount = 0
    discount_rate = 0

    if sushiA + sushiB >= 20:
        discount_rate = 0.2
    elif sushiA + sushiB >= 10:
        discount_rate = 0.1

    current_hour = datetime.now().hour
    if 11 <= current_hour < 14:
        discount_rate += 0.2

    total_discount = total_before_discount * discount_rate
    total_after_discount = total_before_discount - total_discount

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (sushiA, sushiB, discount_applied, total_discount, final_price, order_date) VALUES (%s, %s, %s, %s, %s, %s)",
        (sushiA, sushiB, discount_rate, total_discount, total_after_discount, datetime.now())
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Order added successfully"})

@app.route('/fetch_orders', methods=['GET'])
def fetch_orders():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    
    formatted_orders = []
    for order in orders:
        formatted_order = {
            'order_id': order['order_id'],
            'order_date': order['order_date'],
            'items': [
                {'sushi_type': 'A', 'quantity': order['sushiA'], 'price': order['sushiA'] * 3},
                {'sushi_type': 'B', 'quantity': order['sushiB'], 'price': order['sushiB'] * 4},
            ],
            'discount_applied': order['total_discount'],
            'final_price': order['final_price']
        }
        formatted_orders.append(formatted_order)

    return jsonify(formatted_orders)

@app.route('/test_db_connection', methods=['GET'])
def test_db_connection():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        return jsonify({'message': 'Database connection successful'})
    except mysql.connector.Error as err:
        return jsonify({'message': f'Database connection failed: {err}'})
    
if __name__ == '__main__':
    app.run(debug=True)
