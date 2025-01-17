import sqlite3


def create_users_table():
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        telegram_id BIGINT NOT NULL UNIQUE,
        phone TEXT
        );
        ''')

    database.commit()
    database.close()

# create_users_table()
#

def create_carts_table():
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()

    # carts jadvalini yaratish
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS carts (
        cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES users(user_id),
        total_price DECIMAL(12, 2) DEFAULT 0,
        total_products INTEGER DEFAULT 0
    );
    ''')

    database.commit()
    database.close()

# create_carts_table()


def create_carts_product_table():
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart_products (
        cart_product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name VARCHAR(30),
        quantity INTEGER NOT NULL,
        final_price DECIMAL(12, 2) NOT NULL,
        cart_id INTEGER REFERENCES carts(cart_id),
        
        UNIQUE(product_name, cart_id)
        );
        ''')
    database.commit()
    database.close()

# create_carts_product_table()


def create_categories_table():
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        categories_id INTEGER PRIMARY KEY AUTOINCREMENT,
        categories_name VARCHAR(50) NOT NULL UNIQUE
    );
    ''')
    database.commit()
    database.close()


# create_categories_table()


def insert_categories():
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO categories(categories_name) VALUES
    ('🍔BURGERS'),
    ('🍗CHICKEN'),
    ('🍟APPETIZERS'),
    ('🧁DESSERTS'),
    ('🥤DRINKS'),
    ('🧃KIDS MEAL'),
    ('🍕PIZZA'),
    ('🌯SPINNER'),
    ('🥗SALADS & OTHER'),
    ('🍱COMBO'),
    ('SAUCE')
    ''')
    database.commit()
    database.close()

# insert_categories()


def create_products_table():
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        categories_id INTEGER NOT NULL,
        product_name VARCHAR(50) NOT NULL UNIQUE,
        price DECIMAL(12, 2) NOT NULL,
        image TEXT,
        
        FOREIGN KEY(categories_id) REFERENCES categories(categories_id)
         );
        ''')
    database.commit()
    database.close()

# create_products_table()


def insert_products_table():
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO products(categories_id, product_name, price, image) VALUES
    (1, '🍔JUNIOR BURGER', 19000, 'image/1836a1b7fa69d052d8e4e8b2cc968faa.jpg'),
    (1, '🍔LONGER', 25000, 'image/2a96e6c30071f00441cf36d443c06fc7.jpg'),
    (1, '🍔BIGGER', 29000, 'image/8d312744b2e7402f3761063aed832ca0.jpg'),
    (1, '🍔HAMBURGER', 29000, 'image/877651b2f01f9a4743540cfc63cca829.jpg'),
    (1, '🍔CHEESE BURGER', 31000, 'image/a172ebbfbabb250374f34d23642b72b8.jpg'),
    (1, '🍔CHILI LONGER', 29000, 'image/bafeb84229eb710ebb7c2a87f66be680.jpg'),
    (1, '🍔BEEF LONGER', 29000, 'image/bafeb84229eb710ebb7c2a87f66be680.jpg'),
    (1, '🍔CHICKY BURGER', 22000, 'image/308ca629a03f63d83ec006f1de99a96a.jpg')
    ''')

    database.commit()
    database.close()

# insert_products_table()


def first_name_user(chat_id):
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM users WHERE telegram_id = ?
    ''', (chat_id,))
    user = cursor.fetchone()
    database.close()
    return user


def first_register_user(chat_id,full_name):
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO users(telegram_id, full_name) VALUES(?, ?)
    ''', (chat_id,full_name))
    database.commit()
    database.close()


def update_user_to_finish_register(chat_id, phone):
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
        UPDATE users 
        SET phone = ?
        WHERE telegram_id = ?
    ''', (phone, chat_id))
    database.commit()
    database.close()


def insert_to_cart(chat_id):
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO carts(user_id) VALUES
    (
    (SELECT user_id FROM users WHERE telegram_id = ?)
    )
    ''', (chat_id))
    database.commit()
    database.close()


def get_all_catrgories():
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM categories
    ''')
    categories = cursor.fetchall()
    database.close()
    return categories


def get_products_by_category_id(category_id):
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT product_id, product_name
    FROM products WHERE categories_id = ?
    ''', (category_id,))
    products = cursor.fetchall()
    database.close()
    return products


def get_product_detail(product_id):
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM products WHERE product_id = ?
    ''', (product_id,))
    product = cursor.fetchone()
    database.close()
    return product


def get_user_cart_id(chat_id):
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
        SELECT cart_id FROM carts WHERE chat_id = ?
    ''', (chat_id,))
    result = cursor.fetchone()
    database.close()
    return result[0] if result else None


# def add_price_column():
#     database = sqlite3.connect('loook.db')
#     cursor = database.cursor()
#
#     # `price` ustunini qo'shish
#     cursor.execute('''ALTER TABLE cart_products ADD COLUMN price REAL''')
#
#     database.commit()
#     database.close()
#
# # add_price_column()
#
# def add_unit_price_column():
#     # Ma'lumotlar bazasiga ulanish
#     database = sqlite3.connect('loook.db')
#     cursor = database.cursor()
#
#     # `unit_price` ustunini qo'shish
#     cursor.execute('''ALTER TABLE cart_products ADD COLUMN unit_price REAL''')
#
#     # O'zgartirishlarni saqlash
#     database.commit()
#
#     # Ma'lumotlar bazasini yopish
#     database.close()
#
# # Funksiyani chaqirish
# # add_unit_price_column()





def add_product_to_cart_db(chat_id, product_name, quantity, price):
    # qiymatlar None bo'lishi mumkin, shuning uchun ularni tekshiramiz
    if quantity is None or price is None:
        raise ValueError("Quantity or Price cannot be None")

    database = sqlite3.connect('loook.db')
    cursor = database.cursor()

    # Foydalanuvchining savatini olish yoki yaratish
    cursor.execute('''
    SELECT cart_id FROM carts WHERE user_id = ?
    ''', (chat_id,))
    result = cursor.fetchone()

    if result is None:
        # Savat mavjud emas, yangi savat yaratamiz
        cursor.execute('''
        INSERT INTO carts (user_id, total_price, total_products)
        VALUES (?, 0, 0)
        ''', (chat_id,))
        database.commit()
        cursor.execute('SELECT last_insert_rowid()')
        result = cursor.fetchone()

    cart_id = result[0]  # Savat ID si

    # Savatga mahsulot qo'shish yoki yangilash
    cursor.execute('''
    SELECT cart_product_id, quantity FROM cart_products
    WHERE cart_id = ? AND product_name = ?
    ''', (cart_id, product_name))
    cart_product = cursor.fetchone()

    if cart_product:
        # Mahsulot mavjud, miqdorni yangilaymiz
        cart_product_id, existing_quantity = cart_product
        new_quantity = existing_quantity + quantity
        new_final_price = new_quantity * price

        cursor.execute('''
        UPDATE cart_products
        SET quantity = ?, final_price = ?
        WHERE cart_product_id = ?
        ''', (new_quantity, new_final_price, cart_product_id))
    else:
        # Mahsulot yangi, qo'shamiz
        final_price = quantity * price
        cursor.execute('''
        INSERT INTO cart_products (cart_id, product_name, quantity, price, final_price)
        VALUES (?, ?, ?, ?, ?)
        ''', (cart_id, product_name, quantity, price, final_price))

    database.commit()
    database.close()



def update_total_product_total_price(cart_id):
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
    UPDATE carts
    SET total_products = (
    SELECT SUM(quantity) FROM cart_products
    WHERE cart_id = :cart_id
    ),
    total_price = (
    SELECT SUM(final_price) FROM cart_products
    WHERE cart_id = :cart_id
    )
    WHERE cart_id = :cart_id
    ''', {'cart_id': cart_id})
    database.commit()
    database.close()


def get_cart_products(cart_id):
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT product_name, quantity, final_price
    FROM cart_products
    WHERE cart_id = ?
    ''', (cart_id,))
    products = cursor.fetchall()
    database.close()
    return products



def get_total_products_price(cart_id):
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT total_products, total_price FROM carts WHERE cart_id = ?
    ''', (cart_id,))
    total_products, total_price = cursor.fetchone()
    database.close()
    return total_products, total_price



def get_cart_product_for_delete(cart_id):
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT cart_product_id, product_name
    FROM cart_products
    WHERE cart_id = ?
    ''', (cart_id,))
    cart_products = cursor.fetchall()
    print(f"Savat mahsulotlari: {cart_products}")
    database.close()
    return cart_products


def delete_cart_product_from_database(cart_product_id):
    if not isinstance(cart_product_id, int):
        raise ValueError("Mahsulot ID raqam bo‘lishi kerak.")
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
    DELETE FROM cart_products WHERE cart_product_id = ?
    ''', (cart_product_id,))
    database.commit()
    database.close()




def decrease_cart_product_quantity(cart_product_id, amount):
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()

    # Mahsulotni olish
    cursor.execute('''
    SELECT quantity, price FROM cart_products WHERE cart_product_id = ?
    ''', (cart_product_id,))
    cart_product = cursor.fetchone()

    if cart_product is None:
        raise ValueError(f"Mahsulot {cart_product_id} topilmadi.")

    # Mahsulot ma'lumotlarini ajratamiz
    existing_quantity, price = cart_product

    # quantity va price qiymatlarining None bo'lmasligini tekshiramiz
    if existing_quantity is None or price is None:
        raise ValueError("Mahsulotning quantity yoki price qiymatlari mavjud emas.")

    # Yangi quantity va final_price ni hisoblaymiz
    new_quantity = existing_quantity - amount
    if new_quantity < 0:
        new_quantity = 0  # Mahsulot miqdori manfiy bo'lmasligi kerak

    new_final_price = new_quantity * price

    # Yangilash
    cursor.execute('''
    UPDATE cart_products
    SET quantity = ?, final_price = ?
    WHERE cart_product_id = ?
    ''', (new_quantity, new_final_price, cart_product_id))

    database.commit()
    database.close()





def drop_cart_products_default(cart_id):
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
    DELETE FROM cart_products
    WHERE cart_id = ?
    ''', (cart_id,))
    database.commit()
    database.close()


def orders_check():
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders_check(
    order_check_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id INTEGER REFERENCES carts(cart_id),
    total_price DECIMAL(12, 2) DEFAULT 0,
    total_products INTEGER DEFAULT 0,
    time_order TEXT,
    data_order TEXT
    );
    ''')
    database.commit()
    database.close()


# orders_check()


def order():
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders(
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cart_id INTEGER, -- Savat ID ni saqlash uchun ustun
        order_check_id INTEGER REFERENCES orders_check(order_check_id),
        product_name VARCHAR(100) NOT NULL,
        quantity INTEGER NOT NULL,
        final_price DECIMAL(12, 2) NOT NULL
    );
    ''')
    database.commit()
    database.close()

# order()


def save_order_check(cart_id, total_products, total_price, time_order, date_order):
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO orders_check(cart_id, total_products, total_price, time_order, data_order)
    VALUES (?, ?, ?, ?, ?)
    ''', (cart_id, total_products, total_price, time_order, date_order))
    database.commit()
    database.close()


def get_order_check_id(cart_id):
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT order_check_id FROM orders_check
    WHERE cart_id = ?
    ''', (cart_id,))
    order_check_id = cursor.fetchall()[-1][0]
    database.close()
    return order_check_id


def save_order(order_check_id, product_name, quantity, final_price):
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO orders(order_check_id, product_name, quantity, final_price)
    VALUES(?, ?, ?, ?)
    ''', (order_check_id, product_name, quantity, final_price))
    database.commit()
    database.close()


def get_order_check(cart_id):
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
        SELECT *
        FROM orders_check
        WHERE cart_id = ?
    ''', (cart_id,))
    result = cursor.fetchall()
    database.close()
    return result



def get_detail_order(id):
    database = sqlite3.connect('loook.db')
    cursor = database.cursor()
    cursor.execute('''
        SELECT product_name, quantity, final_price FROM orders
        WHERE order_check_id = ?
    ''', (id,))
    detail_order = cursor.fetchall()
    database.close()
    return detail_order




