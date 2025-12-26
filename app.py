import pyodbc
from flask import Flask, jsonify
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Дозволяє крос-доменні запити



def get_db_connection():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=legion;'
                          'Database=coffeebes;'
                          'Trusted_Connection=yes;')
    return conn

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Оновлений запит з умовою status = 'admin'
        cursor.execute("""
            SELECT id, username, first_name, middle_name, last_name, phone_number, birth_date, shop_id
            FROM users
            WHERE status = 'admin'
        """)

        users = cursor.fetchall()
        if not users:
            return jsonify({'message': 'Немає користувачів зі статусом admin у базі даних'}), 200

        # Формування списку користувачів
        users_list = [
            {
                'id': user[0],
                'username': user[1],
                'first_name': user[2],
                'middle_name': user[3],
                'last_name': user[4],
                'phone_number': user[5],
                'birth_date': user[6].strftime('%Y-%m-%d') if user[6] else None,
                'shop_id': user[7]
            }
            for user in users
        ]

        return jsonify(users_list)
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при роботі з базою даних'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/users', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')  # Отримуємо пароль
        if not username or not password:
            return jsonify({'error': 'Логін та пароль є обов\'язковими'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return jsonify({'message': 'Користувача додано успішно'}), 201
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при додаванні користувача'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", user_id)
        conn.commit()
        return jsonify({'message': 'Користувача видалено успішно'})
    except pyodbc.Error as e:
        if 'REFERENCE' in str(e):
            return jsonify({'error': 'Неможливо видалити користувача, оскільки існують пов\'язані записи'}), 409
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при видаленні користувача'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/check-login', methods=['POST'])
def check_login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'error': 'Логін та пароль є обов\'язковими'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM users WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()

        if result:
            status = result[0]  # Отримуємо статус користувача
            if status == 'prime-admin':
                return jsonify({'status': 'prime-admin', 'message': 'Вітаємо старшого адміна!'}), 200
            elif status == 'admin':
                return jsonify({'status': 'admin', 'message': 'Вітаємо адміна!'}), 200
            elif status == 'user':
                return jsonify({'status': 'user', 'message': 'Вітаємо гостя!'}), 200
            elif status == 'ban':
                return jsonify({'status': 'ban', 'message': 'Вам вхід заборонено!'}), 200
            else:
                return jsonify({'error': 'Невідомий статус користувача'}), 400
        else:
            return jsonify({'exists': False, 'message': 'Логін або пароль невірні.'}), 200

    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при перевірці логіну та пароля'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        last_name = data.get('last_name')
        first_name = data.get('first_name')
        middle_name = data.get('middle_name')
        phone_number = data.get('phone_number')
        birth_date = data.get('birth_date')

        # Перевірка наявності обов'язкових полів
        if not all([username, password, last_name, first_name, middle_name, phone_number, birth_date]):
            return jsonify({'error': 'Всі поля є обов\'язковими'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Запис користувача у таблицю
        cursor.execute("""
            INSERT INTO users (username, password, last_name, first_name, middle_name, phone_number, birth_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
                       (username, password, last_name, first_name, middle_name, phone_number, birth_date))
        conn.commit()

        return jsonify({'message': 'Користувача зареєстровано успішно'}), 201
    except pyodbc.IntegrityError:
        return jsonify({'error': 'Користувач з таким логіном вже існує'}), 409
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при реєстрації'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/admins-count', methods=['GET'])
def get_admins_count():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'admin'")
        result = cursor.fetchone()
        count = result[0] if result else 0
        return jsonify({'admins_count': count})
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при отриманні кількості адмінів'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/users-count', methods=['GET'])
def get_users_count():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'user'")
        result = cursor.fetchone()
        count = result[0] if result else 0
        return jsonify({'users_count': count})
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при отриманні кількості користувачів'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/user-profile', methods=['GET'])
def get_user_profile():
    try:
        # Отримуємо username з параметрів запиту
        username = request.args.get('username')

        if not username:
            return jsonify({'error': 'Логін не вказано'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Оновлений запит, що включає ім'я та по батькові
        cursor.execute("""
            SELECT username, last_name, first_name, middle_name, phone_number
            FROM users
            WHERE username = ?
        """, (username,))

        user = cursor.fetchone()

        if user:
            return jsonify({
                'username': user[0],
                'last_name': user[1],
                'first_name': user[2],
                'middle_name': user[3],
                'phone_number': user[4]
            })
        else:
            return jsonify({'error': 'Користувача не знайдено'}), 404

    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при отриманні профілю користувача'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/update-profile', methods=['POST'])
def update_profile():
    # Отримуємо дані з тіла запиту
    data = request.get_json()

    username = data.get('username')
    first_name = data.get('first_name')
    middle_name = data.get('middle_name')
    last_name = data.get('last_name')
    phone_number = data.get('phone_number')

    if not username:
        return jsonify({'error': 'Username is required'}), 400

    # Підключаємося до бази даних
    conn = get_db_connection()
    cursor = conn.cursor()

    # Оновлюємо дані користувача в базі даних
    cursor.execute('''
        UPDATE users
        SET first_name = ?, middle_name = ?, last_name = ?, phone_number = ?
        WHERE username = ?
    ''', (first_name, middle_name, last_name, phone_number, username))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Profile updated successfully'}), 200

@app.route('/api/guests', methods=['GET'])
def get_guests():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Запит для вибору необхідних даних тільки для гостей
        cursor.execute("""
            SELECT id, username, first_name, middle_name, last_name, phone_number, birth_date, points
            FROM users
            WHERE status = 'user'
        """)

        guests = cursor.fetchall()
        if not guests:
            return jsonify({'message': 'Немає гостей у базі даних'}), 200

        # Формування списку гостей
        guests_list = [
            {
                'id': guest[0],
                'username': guest[1],
                'first_name': guest[2],
                'middle_name': guest[3],
                'last_name': guest[4],
                'phone_number': guest[5],
                'birth_date': guest[6],  # Додаємо дату народження
                'points': guest[7] if guest[7] is not None else 0  # Конвертуємо null в 0
            }
            for guest in guests
        ]

        return jsonify(guests_list)
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при роботі з базою даних'}), 500
    finally:
        if 'conn' in locals():
            conn.close()



@app.route('/api/set-admin/<int:user_id>', methods=['POST'])
def set_admin_status(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET status = 'admin' WHERE id = ?", user_id)
        conn.commit()
        return jsonify({'message': 'Status set to admin successfully'})
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при встановленні статусу admin'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/set-user/<int:user_id>', methods=['POST'])
def set_user_status(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET status = 'user' WHERE id = ?", user_id)
        conn.commit()
        return jsonify({'message': 'Status set to user successfully'})
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при встановленні статусу user'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/set-ban/<int:user_id>', methods=['POST'])
def set_ban_status(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET status = 'ban' WHERE id = ?", user_id)
        conn.commit()
        return jsonify({'message': 'Status set to ban successfully'})
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при встановленні статусу ban'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/shops', methods=['GET'])
def get_shops():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, Street, nomer, loc_desc, photo1, has_bakery FROM shops")
        shops = cursor.fetchall()
        shops_list = []
        for shop in shops:
            shops_list.append({
                'id': shop.id,
                'Street': shop.Street,
                'nomer': shop.nomer,
                'loc_desc': shop.loc_desc,
                'photo1': shop.photo1,
                'has_bakery': shop.has_bakery,
            })
        return jsonify(shops_list)
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при роботі з базою даних'}), 500
    finally:
        if 'conn' in locals():
            conn.close()


@app.route('/api/drinks', methods=['GET'])
def get_drinks():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM drinks")
        drinks = cursor.fetchall()
        drinks_list = []
        for drink in drinks:
            drinks_list.append({
                'id': drink.id,
                'name': drink.name,
            })
        return jsonify(drinks_list)
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при роботі з базою даних'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/drink_sizes', methods=['GET'])
def get_drink_sizes():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ds.drink_id, d.name, ds.size, ds.price FROM drink_sizes ds JOIN drinks d ON ds.drink_id = d.id")
        drink_sizes = cursor.fetchall()
        drink_sizes_list = []
        for drink_size in drink_sizes:
            drink_sizes_list.append({
                'drink_id': drink_size.drink_id,
                'drink_name': drink_size.name,
                'size': drink_size.size,
                'price': float(drink_size.price),
            })
        return jsonify(drink_sizes_list)
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при роботі з базою даних'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/shops-count', methods=['GET'])
def get_shops_count():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM shops")
        result = cursor.fetchone()
        count = result[0] if result else 0
        return jsonify({'shops_count': count})
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при отриманні кількості кав\'ярень'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/bakery', methods=['GET'])
def get_bakery():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price FROM bakery")
        bakery_items = cursor.fetchall()
        bakery_list = []
        for item in bakery_items:
            bakery_list.append({
                'id': item.id,
                'name': item.name,
                'price': float(item.price),
            })
        return jsonify(bakery_list)
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при роботі з базою даних'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

# Створення нового замовлення
@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        shop_id = data.get('shop_id')
        drinks = data.get('drinks', [])
        bakery_items = data.get('bakery_items', [])
        total_price = data.get('total_price', 0)

        if not user_id or not shop_id:
            return jsonify({'error': 'Відсутній user_id або shop_id'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Використовуємо OUTPUT для отримання ID відразу при вставці
            cursor.execute("""
                INSERT INTO orders (user_id, shop_id, status, total_price, order_date)
                OUTPUT INSERTED.id
                VALUES (?, ?, 'pending', ?, GETDATE())
                """, (user_id, shop_id, total_price))

            row = cursor.fetchone()
            if not row:
                raise Exception("Insert failed - no ID returned")

            order_id = row[0]
            print(f"Created order with ID: {order_id}")

            # Додаємо напої до замовлення
            for drink in drinks:
                # Спочатку отримуємо ціну
                cursor.execute("""
                    SELECT price 
                    FROM drink_sizes 
                    WHERE drink_id = ? AND size = ?
                    """, (drink['drink_id'], drink['size']))

                price_row = cursor.fetchone()
                if not price_row:
                    raise Exception(f"Price not found for drink_id={drink['drink_id']}, size={drink['size']}")

                drink_price = price_row[0]

                # Додаємо напій до замовлення
                cursor.execute("""
                    INSERT INTO order_drinks (order_id, drink_id, size, quantity, price)
                    VALUES (?, ?, ?, ?, ?)
                    """, (order_id, drink['drink_id'], drink['size'],
                          drink['quantity'], drink_price))
                print(f"Added drink: order_id={order_id}, drink_id={drink['drink_id']}")

            # Додаємо випічку до замовлення
            for bakery in bakery_items:
                cursor.execute("""
                    SELECT price 
                    FROM bakery 
                    WHERE id = ?
                    """, (bakery['bakery_id'],))

                price_row = cursor.fetchone()
                if not price_row:
                    raise Exception(f"Price not found for bakery_id={bakery['bakery_id']}")

                bakery_price = price_row[0]

                cursor.execute("""
                    INSERT INTO order_bakery (order_id, bakery_id, quantity, price)
                    VALUES (?, ?, ?, ?)
                    """, (order_id, bakery['bakery_id'],
                          bakery['quantity'], bakery_price))
                print(f"Added bakery: order_id={order_id}, bakery_id={bakery['bakery_id']}")

            conn.commit()
            print(f"Order {order_id} committed successfully")
            return jsonify({
                'message': 'Замовлення створено',
                'order_id': order_id,
                'total_price': total_price
            }), 201

        except Exception as e:
            conn.rollback()
            print(f"Error during order creation: {str(e)}")
            raise

    except Exception as e:
        print(f"Error in create_order: {str(e)}")
        return jsonify({'error': f'Помилка при створенні замовлення: {str(e)}'}), 500
    finally:
        if 'conn' in locals():
            conn.close()


@app.route('/api/user-id', methods=['GET'])
def get_user_id():
    try:
        username = request.args.get('username')
        if not username:
            return jsonify({'error': 'Username is required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()

        if result:
            return jsonify({'id': result[0]})
        else:
            return jsonify({'error': 'User not found'}), 404
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при роботі з базою даних'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/get_all_users', methods=['GET'])
def get_all_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, first_name, middle_name, last_name, phone_number, birth_date, shop_id, status
            FROM users
            WHERE status <> 'ban'
        """)
        users = cursor.fetchall()
        if not users:
            return jsonify({'message': 'Немає користувачів у базі даних'}), 200

        # Формування списку користувачів
        users_list = [
            {
                'id': user[0],
                'username': user[1],
                'first_name': user[2],
                'middle_name': user[3],
                'last_name': user[4],
                'phone_number': user[5],
                'birth_date': user[6].strftime('%Y-%m-%d') if user[6] else None,
                'shop_id': user[7],
                'status': user[8]  # Додаємо статус користувача
            }
            for user in users
        ]

        return jsonify(users_list)
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при роботі з базою даних'}), 500
    finally:
        if 'conn' in locals():
            conn.close()



@app.route('/api/orders', methods=['GET'])
def get_orders():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, user_id, shop_id, status, total_price, order_date FROM orders")
        orders = cursor.fetchall()
        orders_list = []
        for order in orders:
            orders_list.append({
                'id': order.id,
                'user_id': order.user_id,
                'shop_id': order.shop_id,
                'status': order.status,
                'total_price': float(order.total_price),
                'order_date': order.order_date.strftime('%Y-%m-%d %H:%M:%S') if order.order_date else None,
            })
        return jsonify(orders_list)
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при роботі з базою даних'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/order-bakery/<int:order_id>', methods=['GET'])
def get_order_bakery(order_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT bakery_id, quantity, price FROM order_bakery WHERE order_id = ?", order_id)
        bakery_items = cursor.fetchall()
        bakery_list = []
        for item in bakery_items:
            bakery_list.append({
                'bakery_id': item.bakery_id,
                'quantity': item.quantity,
                'price': float(item.price),
            })
        return jsonify(bakery_list)
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при роботі з базою даних'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/order-drinks/<int:order_id>', methods=['GET'])
def get_order_drinks(order_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT drink_id, size, quantity, price FROM order_drinks WHERE order_id = ?", order_id)
        drink_items = cursor.fetchall()
        drinks_list = []
        for item in drink_items:
            drinks_list.append({
                'drink_id': item.drink_id,
                'size': item.size,
                'quantity': item.quantity,
                'price': float(item.price),
            })
        return jsonify(drinks_list)
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при роботі з базою даних'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/orders-idsort/<int:user_id>', methods=['GET'])
def get_orders_idsort(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, user_id, shop_id, status, total_price, order_date FROM orders WHERE user_id = ? ORDER BY order_date DESC", user_id)
        orders = cursor.fetchall()
        orders_list = []
        for order in orders:
            orders_list.append({
                'id': order.id,
                'user_id': order.user_id,
                'shop_id': order.shop_id,
                'status': order.status,
                'total_price': float(order.total_price),
                'order_date': order.order_date.strftime('%Y-%m-%d %H:%M:%S') if order.order_date else None,
            })
        return jsonify(orders_list)
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при роботі з базою даних'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/bakery-names', methods=['POST'])
def get_bakery_names():
    try:
        print("Received request for bakery names") # Додаємо логування
        data = request.get_json()
        print("Received data:", data) # Логуємо отримані дані

        bakery_ids = data.get('bakery_ids', [])
        print("Extracted bakery_ids:", bakery_ids) # Логуємо ID випічки

        if not bakery_ids:
            print("No bakery IDs provided") # Логуємо помилку
            return jsonify({'error': 'No bakery IDs provided'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Create a placeholder string for the SQL query
        placeholders = ', '.join('?' for _ in bakery_ids)
        query = f"SELECT id, name FROM bakery WHERE id IN ({placeholders})"
        print("SQL Query:", query) # Логуємо SQL запит
        print("Parameters:", bakery_ids) # Логуємо параметри

        cursor.execute(query, bakery_ids)
        bakery_items = cursor.fetchall()
        print("Fetched items:", bakery_items) # Логуємо отримані дані

        bakery_names = {}
        for row in bakery_items:
            bakery_names[str(row[0])] = row[1]

        print("Returning:", bakery_names) # Логуємо результат
        return jsonify(bakery_names)

    except Exception as e:
        print(f"Error in get_bakery_names: {str(e)}") # Логуємо помилку
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        if 'conn' in locals():
            conn.close()


@app.route('/api/drink-names', methods=['POST'])
def get_drink_names():
    try:
        print("Received request for drink names") # Додаємо логування
        data = request.get_json()
        print("Received data:", data) # Логуємо отримані дані

        drink_ids = data.get('drink_ids', [])
        print("Extracted drink_ids:", drink_ids) # Логуємо ID напоїв

        if not drink_ids:
            print("No drink IDs provided") # Логуємо помилку
            return jsonify({'error': 'No drink IDs provided'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Create a placeholder string for the SQL query
        placeholders = ', '.join('?' for _ in drink_ids)
        query = f"SELECT id, name FROM drinks WHERE id IN ({placeholders})"
        print("SQL Query:", query) # Логуємо SQL запит
        print("Parameters:", drink_ids) # Логуємо параметри

        cursor.execute(query, drink_ids)
        drink_items = cursor.fetchall()
        print("Fetched items:", drink_items) # Логуємо отримані дані

        drink_names = {}
        for row in drink_items:
            drink_names[str(row[0])] = row[1]

        print("Returning:", drink_names) # Логуємо результат
        return jsonify(drink_names)

    except Exception as e:
        print(f"Error in get_drink_names: {str(e)}") # Логуємо помилку
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/shop-addresses', methods=['POST'])
def get_shop_addresses():
    try:
        print("Received request for shop addresses") # Додаємо логування
        data = request.get_json()
        print("Received data:", data) # Логуємо отримані дані

        shop_ids = data.get('shop_ids', [])
        print("Extracted shop_ids:", shop_ids) # Логуємо ID кав'ярень

        if not shop_ids:
            print("No shop IDs provided") # Логуємо помилку
            return jsonify({'error': 'No shop IDs provided'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Create a placeholder string for the SQL query
        placeholders = ', '.join('?' for _ in shop_ids)
        query = f"SELECT id, Street, nomer, loc_desc FROM shops WHERE id IN ({placeholders})"
        print("SQL Query:", query) # Логуємо SQL запит
        print("Parameters:", shop_ids) # Логуємо параметри

        cursor.execute(query, shop_ids)
        shop_items = cursor.fetchall()
        print("Fetched items:", shop_items) # Логуємо отримані дані

        shop_addresses = {}
        for row in shop_items:
            shop_addresses[str(row[0])] = f"{row[1]} {row[2]}, {row[3]}"

        print("Returning:", shop_addresses) # Логуємо результат
        return jsonify(shop_addresses)

    except Exception as e:
        print(f"Error in get_shop_addresses: {str(e)}") # Логуємо помилку
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/user-details', methods=['POST'])
def get_user_details():
    try:
        print("Received request for user details") # Додаємо логування
        data = request.get_json()
        print("Received data:", data) # Логуємо отримані дані

        user_ids = data.get('user_ids', [])
        print("Extracted user_ids:", user_ids) # Логуємо ID користувачів

        if not user_ids:
            print("No user IDs provided") # Логуємо помилку
            return jsonify({'error': 'No user IDs provided'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Create a placeholder string for the SQL query
        placeholders = ', '.join('?' for _ in user_ids)
        query = f"SELECT id, last_name, first_name, middle_name FROM users WHERE id IN ({placeholders})"
        print("SQL Query:", query) # Логуємо SQL запит
        print("Parameters:", user_ids) # Логуємо параметри

        cursor.execute(query, user_ids)
        user_items = cursor.fetchall()
        print("Fetched items:", user_items) # Логуємо отримані дані

        user_details = {}
        for row in user_items:
            user_details[str(row[0])] = f"{row[1]} {row[2]} {row[3]}"

        print("Returning:", user_details) # Логуємо результат
        return jsonify(user_details)

    except Exception as e:
        print(f"Error in get_user_details: {str(e)}") # Логуємо помилку
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/shop-id', methods=['GET'])
def get_shop_id():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT shop_id FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()

        if result:
            return jsonify({'shop_id': result[0]})
        else:
            return jsonify({'error': 'User not found'}), 404
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при роботі з базою даних'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/record-payment', methods=['POST'])
def record_payment():
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        user_id = data.get('user_id')
        payment_method = data.get('payment_method')

        if not order_id or not user_id:
            return jsonify({'error': 'All fields are required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        if payment_method == 'points':
            # Fetch the total price of the order
            cursor.execute("SELECT total_price FROM orders WHERE id = ?", (order_id,))
            row = cursor.fetchone()
            if not row:
                print(f"Order not found for order_id: {order_id}")
                return jsonify({'error': 'Order not found'}), 404

            total_price = row[0]
            points_to_deduct = round(total_price / 10)

            # Fetch the user's current points
            cursor.execute("SELECT points FROM users WHERE id = ?", (user_id,))
            user_row = cursor.fetchone()
            if not user_row:
                print(f"User not found for user_id: {user_id}")
                return jsonify({'error': 'User not found'}), 404

            current_points = user_row[0]

            # Check if the user has enough points
            if current_points < points_to_deduct:
                print(f"Not enough points for user_id: {user_id}, required: {points_to_deduct}, available: {current_points}")
                return jsonify({'error': 'Not enough points to complete the payment'}), 400

            # Deduct points from the user's account
            cursor.execute("UPDATE users SET points = points - ? WHERE id = ?", (points_to_deduct, user_id))
        else:
            # Handle card payment
            card_number = data.get('card_number')
            expiration_date = data.get('expiration_date')
            cvv = data.get('cvv')
            cursor.execute("INSERT INTO payments (order_id, user_id, card_number, expiration_date, cvv) VALUES (?, ?, ?, ?, ?)",
                           (order_id, user_id, card_number, expiration_date, cvv))

        # Update order status to 'paid'
        cursor.execute("UPDATE orders SET status = 'paid' WHERE id = ?", order_id)

        conn.commit()
        return jsonify({'message': 'Payment recorded and order status updated successfully'}), 200
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        if 'conn' in locals():
            conn.close()






@app.route('/api/update-order-status/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    try:
        data = request.get_json()
        new_status = data.get('status')

        if not new_status:
            return jsonify({'error': 'Status is required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Update order status
        cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
        conn.commit()

        return jsonify({'message': 'Order status updated successfully'}), 200
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/payments/<int:order_id>', methods=['GET'])
def get_payment_details(order_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT payment_date, card_number FROM payments WHERE order_id = ?", order_id)
        payment = cursor.fetchone()
        if payment:
            return jsonify({
                'payments_date': payment.payment_date.strftime('%Y-%m-%d %H:%M:%S') if payment.payment_date else None,
                'card_number': payment.card_number
            })
        else:
            return jsonify({'error': 'Payment not found'}), 404
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при роботі з базою даних'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/vacancies', methods=['POST'])
def create_vacancy():
    try:
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        salary = data.get('salary')

        if not title or not description or not salary:
            return jsonify({'error': 'Всі поля є обов\'язковими'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO vacancies (title, description, salary) VALUES (?, ?, ?)", (title, description, salary))
        conn.commit()

        # Fetch the newly created vacancy
        cursor.execute("SELECT id, title, description, salary FROM vacancies WHERE title = ? AND description = ? AND salary = ?", (title, description, salary))
        vacancy = cursor.fetchone()

        if vacancy:
            return jsonify({
                'id': vacancy.id,
                'title': vacancy.title,
                'description': vacancy.description,
                'salary': vacancy.salary,
            }), 201
        else:
            return jsonify({'error': 'Помилка створення вакансії'}), 500
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при створенні вакансії'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/vacancies', methods=['GET'])
def get_vacancies():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description, salary FROM vacancies")
        vacancies = cursor.fetchall()
        vacancies_list = []
        for vacancy in vacancies:
            vacancies_list.append({
                'id': vacancy.id,
                'title': vacancy.title,
                'description': vacancy.description,
                'salary': vacancy.salary,
            })
        return jsonify(vacancies_list)
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при роботі з базою даних'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/vacancies/<int:vacancy_id>', methods=['DELETE'])
def delete_vacancy(vacancy_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vacancies WHERE id = ?", vacancy_id)
        conn.commit()
        return jsonify({'message': 'Вакансію видалено успішно'})
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при видаленні вакансії'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/vacancies/<int:vacancy_id>', methods=['PUT'])
def update_vacancy(vacancy_id):
    try:
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        salary = data.get('salary')

        if not title or not description or not salary:
            return jsonify({'error': 'Всі поля є обов\'язковими'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE vacancies SET title = ?, description = ?, salary = ? WHERE id = ?", (title, description, salary, vacancy_id))
        conn.commit()

        # Fetch the updated vacancy
        cursor.execute("SELECT id, title, description, salary FROM vacancies WHERE id = ?", vacancy_id)
        vacancy = cursor.fetchone()

        if vacancy:
            return jsonify({
                'id': vacancy.id,
                'title': vacancy.title,
                'description': vacancy.description,
                'salary': vacancy.salary,
            }), 200
        else:
            return jsonify({'error': 'Помилка оновлення вакансії'}), 500
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при оновленні вакансії'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/feedback', methods=['POST'])
def create_feedback():
    try:
        data = request.get_json()
        user_id = data.get('userId')
        vacancy_id = data.get('vacancyId')
        first_name = data.get('firstName')
        middle_name = data.get('middleName')
        last_name = data.get('lastName')
        phone = data.get('phone')
        contact_method = data.get('contactMethod')
        contact_detail = data.get('contactDetail')
        residence = data.get('residence')
        experience = data.get('experience')
        about = data.get('about')
        why_coffe_boss = data.get('whyCoffeBoss')

        if not all([user_id, vacancy_id, first_name, middle_name, last_name, phone, contact_method, residence, experience, about, why_coffe_boss]):
            return jsonify({'error': 'Всі поля є обов\'язковими'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO feedback (user_id, vacancy_id, first_name, middle_name, last_name, phone, contact_method, contact_detail, residence, experience, about, why_coffe_boss)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, vacancy_id, first_name, middle_name, last_name, phone, contact_method, contact_detail, residence, experience, about, why_coffe_boss))
        conn.commit()

        return jsonify({'message': 'Feedback submitted successfully'}), 201
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при збереженні відгуку'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/feedback', methods=['GET'])
def get_feedback():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM feedback")
        feedback_list = []
        for row in cursor.fetchall():
            feedback_list.append({
                'id': row.id,
                'user_id': row.user_id,
                'vacancy_id': row.vacancy_id,
                'first_name': row.first_name,
                'middle_name': row.middle_name,
                'last_name': row.last_name,
                'phone': row.phone,
                'contact_method': row.contact_method,
                'contact_detail': row.contact_detail,
                'residence': row.residence,
                'experience': row.experience,
                'about': row.about,
                'why_coffe_boss': row.why_coffe_boss,
                'created_at': row.created_at.strftime('%Y-%m-%d %H:%M:%S') if row.created_at else None,
                'shop_id': row.shop_id  # Include shop_id in the response
            })
        return jsonify(feedback_list)
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при роботі з базою даних'}), 500
    finally:
        if 'conn' in locals():
            conn.close()


@app.route('/api/feedback/<int:feedback_id>/assign-shop', methods=['PUT'])
def assign_shop_to_feedback(feedback_id):
    try:
        data = request.get_json()
        shop_id = data.get('shop_id')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE feedback SET shop_id = ? WHERE id = ?", (shop_id, feedback_id))
        conn.commit()

        return jsonify({'message': 'Shop assigned to feedback successfully'}), 200
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/schedule', methods=['POST'])
def create_schedule():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        shop_id = data.get('shop_id')
        work_date = data.get('work_date')
        period = data.get('period')

        if not all([user_id, shop_id, work_date, period]):
            return jsonify({'error': 'Всі поля є обов\'язковими'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO schedule (user_id, shop_id, work_date, period) VALUES (?, ?, ?, ?)",
                       (user_id, shop_id, work_date, period))
        conn.commit()
        return jsonify({'message': 'Графік додано успішно'}), 201
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при додаванні графіка'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/schedule', methods=['GET'])
def get_schedule():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, user_id, shop_id, work_date, period FROM schedule")
        schedule = cursor.fetchall()
        schedule_list = []
        for item in schedule:
            schedule_list.append({
                'id': item.id,  # Ensure id is included
                'user_id': item.user_id,
                'shop_id': item.shop_id,
                'work_date': item.work_date.strftime('%Y-%m-%d'),
                'period': item.period,
            })
        return jsonify(schedule_list)
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при отриманні графіка'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/schedule/<int:schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM schedule WHERE id = ?", schedule_id)
        conn.commit()
        return jsonify({'message': 'Графік видалено успішно'})
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при видаленні графіка'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/user-points/<int:user_id>', methods=['GET'])
def get_user_points(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT points FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        if result:
            return jsonify({'points': result[0]})
        else:
            return jsonify({'error': 'User not found'}), 404
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        if 'conn' in locals():
            conn.close()


@app.route('/api/update-points/<int:user_id>', methods=['PUT'])
def update_points(user_id):
    try:
        data = request.get_json()
        points_to_add = data.get('points')

        if points_to_add is None:
            return jsonify({'error': 'Points value is required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Update the points for the user, treating null as 0
        cursor.execute("UPDATE users SET points = COALESCE(points, 0) + ? WHERE id = ?", (points_to_add, user_id))
        conn.commit()

        return jsonify({'message': 'Points updated successfully'}), 200
    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при оновленні балів'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/generate-code', methods=['POST'])
def generate_code():
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        code = data.get('code')

        if not order_id or not code:
            return jsonify({'error': 'Order ID and code are required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if a code already exists for the given order_id
        cursor.execute("SELECT COUNT(*) FROM luckycheck WHERE order_id = ?", (order_id,))
        result = cursor.fetchone()
        if result and result[0] > 0:
            return jsonify({'error': 'Code already generated for this order'}), 409

        # Insert the new code
        cursor.execute("INSERT INTO luckycheck (order_id, code, status) VALUES (?, ?, ?)", (order_id, code, 'active'))
        conn.commit()

        return jsonify({'message': 'Code generated and saved successfully'}), 201
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/get-generated-code/<int:order_id>', methods=['GET'])
def get_generated_code(order_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT code FROM luckycheck WHERE order_id = ?", (order_id,))
        result = cursor.fetchone()

        if result:
            return jsonify({'code': result[0]}), 200
        else:
            return jsonify({'message': 'No code generated for this order'}), 404
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/verify-lucky-code', methods=['POST'])
def verify_lucky_code():
    try:
        data = request.get_json()
        print("Received data:", data)  # Log the received data

        order_id = data.get('order_id')
        code = data.get('code')

        if not order_id or not code:
            print("Missing order_id or code")  # Log the error
            return jsonify({'error': 'Order ID and code are required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the code exists and is active
        cursor.execute("SELECT status FROM luckycheck WHERE code = ?", (code,))
        result = cursor.fetchone()

        print("Query result:", result)  # Log the query result

        if result and result[0] == 'active':
            # Update the order status to 'paid'
            cursor.execute("UPDATE orders SET status = 'paid' WHERE id = ?", (order_id,))
            # Update the code status to 'used'
            cursor.execute("UPDATE luckycheck SET status = 'used' WHERE code = ?", (code,))
            conn.commit()
            return jsonify({'message': 'Payment confirmed and order status updated successfully'}), 200
        else:
            print("Invalid or inactive code")  # Log the error
            return jsonify({'error': 'Invalid or inactive code'}), 400
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/update-shop/<int:user_id>', methods=['POST'])
def update_shop(user_id):
    try:
        data = request.get_json()
        shop_id = data.get('shop_id')

        if not shop_id:
            return jsonify({'error': 'Shop ID is required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET shop_id = ? WHERE id = ?", (shop_id, user_id))
        conn.commit()

        return jsonify({'message': 'Shop ID updated successfully'}), 200
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    try:
        file = request.files['file']
        if file:
            image_data = file.read()
            image_name = file.filename

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO gallery (image_data, image_name) VALUES (?, ?)",
                           (image_data, image_name))
            conn.commit()
            return jsonify({'message': 'Image uploaded successfully'}), 201
        else:
            return jsonify({'error': 'No file uploaded'}), 400
    except Exception as e:
        print(f"Error uploading image: {e}")
        return jsonify({'error': 'Error uploading image'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/gallery', methods=['GET'])
def get_gallery():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, image_name, upload_date FROM gallery")
        images = cursor.fetchall()
        images_list = []
        for image in images:
            images_list.append({
                'id': image.id,
                'image_name': image.image_name,
                'upload_date': image.upload_date.strftime('%Y-%m-%d %H:%M:%S') if image.upload_date else None,
            })
        return jsonify(images_list)
    except Exception as e:
        print(f"Error fetching gallery: {e}")
        return jsonify({'error': 'Error fetching gallery'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/delete-image/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM gallery WHERE id = ?", image_id)
        conn.commit()
        return jsonify({'message': 'Image deleted successfully'})
    except Exception as e:
        print(f"Error deleting image: {e}")
        return jsonify({'error': 'Error deleting image'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/get-image/<int:image_id>', methods=['GET'])
def get_image(image_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT image_data FROM gallery WHERE id = ?", image_id)
        row = cursor.fetchone()
        if row:
            image_data = row.image_data
            return app.response_class(image_data, mimetype='image/jpeg')
        else:
            return jsonify({'error': 'Image not found'}), 404
    except Exception as e:
        print(f"Error fetching image: {e}")
        return jsonify({'error': 'Error fetching image'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/send-message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')
        content = data.get('content')

        if not sender_id or not receiver_id or not content:
            return jsonify({'error': 'All fields are required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (sender_id, receiver_id, content) VALUES (?, ?, ?)",
                       (sender_id, receiver_id, content))
        conn.commit()

        return jsonify({'message': 'Message sent successfully'}), 201
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/get-messages', methods=['GET'])
def get_messages():
    try:
        sender_id = request.args.get('sender_id')
        receiver_id = request.args.get('receiver_id')

        if not sender_id or not receiver_id:
            return jsonify({'error': 'Both sender_id and receiver_id are required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, sender_id, receiver_id, message_time, content
            FROM messages
            WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
            ORDER BY message_time ASC
        """, (sender_id, receiver_id, receiver_id, sender_id))

        messages = cursor.fetchall()
        messages_list = []
        for message in messages:
            messages_list.append({
                'id': message.id,
                'sender_id': message.sender_id,
                'receiver_id': message.receiver_id,
                'message_time': message.message_time.strftime('%Y-%m-%d %H:%M:%S') if message.message_time else None,
                'content': message.content,
            })

        return jsonify(messages_list)
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/user-profile-by-id/<int:user_id>', methods=['GET'])
def get_user_profile_by_id(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT username, last_name, first_name, middle_name, phone_number
            FROM users
            WHERE id = ?
        """, (user_id,))

        user = cursor.fetchone()

        if user:
            return jsonify({
                'username': user[0],
                'last_name': user[1],
                'first_name': user[2],
                'middle_name': user[3],
                'phone_number': user[4]
            })
        else:
            return jsonify({'error': 'User not found'}), 404

    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/delete-message/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages WHERE id = ?", message_id)
        conn.commit()
        return jsonify({'message': 'Message deleted successfully'}), 200
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/update-message/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    try:
        data = request.get_json()
        content = data.get('content')

        if not content:
            return jsonify({'error': 'Content is required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE messages SET content = ? WHERE id = ?", (content, message_id))
        conn.commit()
        return jsonify({'message': 'Message updated successfully'}), 200
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/get-prime-admin-users', methods=['GET'])
def get_prime_admin_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, last_name, first_name, middle_name FROM users WHERE status = 'prime-admin'")
        users = cursor.fetchall()
        users_list = []
        for user in users:
            users_list.append({
                'id': user.id,
                'username': user.username,
                'last_name': user.last_name,
                'first_name': user.first_name,
                'middle_name': user.middle_name,
            })
        return jsonify(users_list)
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        if 'conn' in locals():
            conn.close()


@app.route('/api/upload-avatar/<int:user_id>', methods=['POST'])
def upload_avatar(user_id):
    try:
        file = request.files['file']
        if file:
            avatar_data = file.read()
            image_name = file.filename

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET avatar = ? WHERE id = ?", (avatar_data, user_id))
            conn.commit()
            return jsonify({'message': 'Avatar uploaded successfully'}), 200
        else:
            return jsonify({'error': 'No file uploaded'}), 400
    except Exception as e:
        print(f"Error uploading avatar: {e}")
        return jsonify({'error': 'Error uploading avatar'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/get-avatar/<int:user_id>', methods=['GET'])
def get_avatar(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT avatar FROM users WHERE id = ?", user_id)
        row = cursor.fetchone()
        if row and row.avatar:
            return app.response_class(row.avatar, mimetype='image/jpeg')
        else:
            return jsonify({'error': 'Avatar not found'}), 404
    except Exception as e:
        print(f"Error fetching avatar: {e}")
        return jsonify({'error': 'Error fetching avatar'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, user_id, shop_id, status, total_price, order_date FROM orders WHERE id = ?", (order_id,))
        order = cursor.fetchone()

        if not order:
            return jsonify({'error': 'Order not found'}), 404

        total_price = order.total_price
        converted_total_price = round(total_price / 10)  # Convert total price to points

        order_details = {
            'id': order.id,
            'user_id': order.user_id,
            'shop_id': order.shop_id,
            'status': order.status,
            'total_price': float(total_price),
            'converted_total_price': converted_total_price,  # Include converted total price
            'order_date': order.order_date.strftime('%Y-%m-%d %H:%M:%S') if order.order_date else None,
        }

        return jsonify(order_details)
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/upload-menu-image/<int:drink_id>', methods=['POST'])
def upload_menu_image(drink_id):
    try:
        file = request.files['file']
        if file:
            image_data = file.read()
            image_name = file.filename

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE drinks SET image = ? WHERE id = ?", (image_data, drink_id))
            conn.commit()
            return jsonify({'message': 'Menu image uploaded successfully'}), 200
        else:
            return jsonify({'error': 'No file uploaded'}), 400
    except Exception as e:
        print(f"Error uploading menu image: {e}")
        return jsonify({'error': 'Error uploading menu image'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/get-menu-image/<int:drink_id>', methods=['GET'])
def get_menu_image(drink_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT image FROM drinks WHERE id = ?", drink_id)
        row = cursor.fetchone()
        if row and row.image:
            return app.response_class(row.image, mimetype='image/jpeg')
        else:
            return jsonify({'error': 'Menu image not found'}), 404
    except Exception as e:
        print(f"Error fetching menu image: {e}")
        return jsonify({'error': 'Error fetching menu image'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/upload-bakery-image/<int:bakery_id>', methods=['POST'])
def upload_bakery_image(bakery_id):
    try:
        file = request.files['file']
        if file:
            image_data = file.read()
            image_name = file.filename

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE bakery SET image = ? WHERE id = ?", (image_data, bakery_id))
            conn.commit()
            return jsonify({'message': 'Bakery image uploaded successfully'}), 200
        else:
            return jsonify({'error': 'No file uploaded'}), 400
    except Exception as e:
        print(f"Error uploading bakery image: {e}")
        return jsonify({'error': 'Error uploading bakery image'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/get-bakery-image/<int:bakery_id>', methods=['GET'])
def get_bakery_image(bakery_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT image FROM bakery WHERE id = ?", bakery_id)
        row = cursor.fetchone()
        if row and row.image:
            return app.response_class(row.image, mimetype='image/jpeg')
        else:
            return jsonify({'error': 'Bakery image not found'}), 404
    except Exception as e:
        print(f"Error fetching bakery image: {e}")
        return jsonify({'error': 'Error fetching bakery image'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/login-check', methods=['POST'])
def login_check():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'error': 'Логін та пароль є обов\'язковими'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the username exists
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()

        if result:
            stored_password = result[0]  # Get the stored password

            # Check if the password matches
            if stored_password == password:
                return jsonify({'exists': True, 'message': 'Логін та пароль вірні.'}), 200
            else:
                return jsonify({'exists': False, 'message': 'Пароль невірний.'}), 200
        else:
            return jsonify({'exists': False, 'message': 'Логін невірний.'}), 200

    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при перевірці логіну та пароля'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/change-password', methods=['POST'])
def change_password():
    try:
        data = request.get_json()
        username = data.get('username')
        newPassword = data.get('newPassword')

        if not username or not newPassword:
            return jsonify({'error': 'Логін та новий пароль є обов\'язковими'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Update the password in the database
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (newPassword, username))
        conn.commit()

        return jsonify({'message': 'Пароль успішно змінено'}), 200

    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при зміні пароля'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/login___check', methods=['POST'])
def login___check():
    try:
        data = request.get_json()
        username = data.get('username')
        phone_number = data.get('phone_number')
        if not username or not phone_number:
            return jsonify({'error': 'Логін та номер телефону є обов\'язковими'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the username and phone number exist
        cursor.execute("SELECT phone_number FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()

        if result:
            stored_phone_number = result[0]  # Get the stored phone number

            # Check if the phone number matches
            if stored_phone_number == phone_number:
                return jsonify({'exists': True, 'message': 'Логін та номер телефону вірні.'}), 200
            else:
                return jsonify({'exists': False, 'message': 'Номер телефону невірний.'}), 200
        else:
            return jsonify({'exists': False, 'message': 'Логін невірний.'}), 200

    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при перевірці логіну та номера телефону'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/recover___password', methods=['POST'])
def recover___password():
    try:
        data = request.get_json()
        username = data.get('username')
        newPassword = data.get('newPassword')

        if not username or not newPassword:
            return jsonify({'error': 'Логін та новий пароль є обов\'язковими'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Update the password in the database
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (newPassword, username))
        conn.commit()

        return jsonify({'message': 'Пароль успішно змінено'}), 200

    except pyodbc.Error as e:
        print(f"Помилка бази даних: {e}")
        return jsonify({'error': 'Сталася помилка при зміні пароля'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/pointorder', methods=['POST'])
def create_pointorder():
    try:
        data = request.get_json()
        personality = data.get('personality')
        number = data.get('number')
        type_delivery = data.get('type_delivery')
        deliveryOption = data.get('deliveryOption')
        city = data.get('city')
        branchNumber = data.get('branchNumber')
        postomatNumber = data.get('postomatNumber')
        address = data.get('address')
        cafeAddress = data.get('cafeAddress')
        orderDetails = data.get('orderDetails')

        if not all([personality, number, type_delivery, orderDetails]):
            return jsonify({'error': 'All fields are required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pointorder (personality, number, type_delivery, deliveryOption, city, branchNumber, postomatNumber, address, cafeAddress, orderDetails)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (personality, number, type_delivery, deliveryOption, city, branchNumber, postomatNumber, address, cafeAddress, orderDetails))
        conn.commit()

        return jsonify({'message': 'Point order created successfully'}), 201
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/update-user-points/<int:user_id>', methods=['PUT'])
def update_user_points(user_id):
    try:
        data = request.get_json()
        points_to_deduct = data.get('points')

        if points_to_deduct is None:
            return jsonify({'error': 'Points value is required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch the current points
        cursor.execute("SELECT points FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        if result:
            current_points = result[0]
            if current_points < points_to_deduct:
                return jsonify({'error': 'Not enough points'}), 400

            # Update the points for the user, treating null as 0
            cursor.execute("UPDATE users SET points = ? WHERE id = ?", (current_points - points_to_deduct, user_id))
            conn.commit()

            return jsonify({'message': 'Points updated successfully'}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/pointorders', methods=['GET'])
def get_pointorders():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, personality, number, type_delivery, deliveryOption, city, branchNumber, postomatNumber, address, cafeAddress, orderDetails, created_at, status
            FROM pointorder
        """)
        pointorders = cursor.fetchall()
        pointorders_list = []
        for order in pointorders:
            pointorders_list.append({
                'id': order.id,
                'personality': order.personality,
                'number': order.number,
                'type_delivery': order.type_delivery,
                'deliveryOption': order.deliveryOption,
                'city': order.city,
                'branchNumber': order.branchNumber,
                'postomatNumber': order.postomatNumber,
                'address': order.address,
                'cafeAddress': order.cafeAddress,
                'orderDetails': order.orderDetails,
                'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S') if order.created_at else None,
                'status': order.status,
            })
        return jsonify(pointorders_list)
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/update-bonus-status/<int:order_id>', methods=['PUT'])
def update_bonus_status(order_id):
    try:
        data = request.get_json()
        new_status = data.get('status')

        if not new_status:
            return jsonify({'error': 'Status is required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Update order status
        cursor.execute("UPDATE pointorder SET status = ? WHERE id = ?", (new_status, order_id))
        conn.commit()

        return jsonify({'message': 'Bonus status updated successfully'}), 200
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        if 'conn' in locals():
            conn.close()



if __name__ == '__main__':
    app.run(debug=True)

