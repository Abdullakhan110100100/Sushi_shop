from flask import Flask, request, jsonify
from datetime import datetime
import mysql.connector
import random


app = Flask(__name__)
from flask_cors import CORS
CORS(app)


order_id_global = 0

# Database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='', # SQLDeRe001#
        database='sushi_shop'
    )
    return conn

def generate_unique_order_id():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    while True:
        order_id = random.randint(1000000000, 9999999999)
        cursor.execute("SELECT 1 FROM orders WHERE order_id = %s", (order_id,))
        if cursor.fetchone() is None:
            break

    cursor.close()
    conn.close()
    return order_id

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    # print('+++++++++++++++++++++++++++++Entered add to cart++++++++++++++++++++++++++++++++++++++++')
    global order_id_global
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

    order_id = generate_unique_order_id()
    
    order_id_global = order_id

    total_discount = total_before_discount * discount_rate
    total_after_discount = total_before_discount - total_discount

    conn = get_db_connection()
    
    cursor = conn.cursor()
    
    try:
        # print((order_id,sushiA, sushiB, discount_rate, total_discount, total_after_discount, datetime.now() ))
        cursor.execute(
            "INSERT INTO new_orders (order_id,sushiA, sushiB, discount_applied, total_discount, final_price, order_date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (order_id,sushiA, sushiB, discount_rate, total_discount, total_after_discount, datetime.now() )
        )
        conn.commit()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")  # Debug statement
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Order added successfully", "order_id": order_id})

@app.route('/fetch_orders', methods=['GET'])
def fetch_orders():
    
    conn = get_db_connection()
    
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute(f"SELECT * FROM new_orders WHERE order_id = {order_id_global};")
    

    orders = cursor.fetchall()
    
    if orders == []:
        raise Exception('Order is empty')
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
