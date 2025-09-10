import sqlite3

# Connect to SQLite database (creates if doesn't exist)
conn = sqlite3.connect('ecommerce.db')
cursor = conn.cursor()

# Create products table
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT
)
''')

# Create orders table
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    total REAL NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products (id)
)
''')

# Seed sample products
products = [
    ('Laptop', 999.99, 'High-performance laptop for work and gaming'),
    ('Mouse', 29.99, 'Ergonomic wireless mouse'),
    ('Keyboard', 79.99, 'Mechanical keyboard with RGB lighting'),
    ('Monitor', 299.99, '27-inch 4K UHD monitor'),
    ('Headphones', 149.99, 'Wireless noise-cancelling headphones')
]

cursor.executemany('INSERT INTO products (name, price, description) VALUES (?, ?, ?)', products)

# Seed sample orders
orders = [
    (1, 1, 999.99),   # 1 Laptop
    (2, 2, 59.98),    # 2 Mice
    (3, 1, 79.99),    # 1 Keyboard
    (4, 1, 299.99),   # 1 Monitor
    (5, 1, 149.99)    # 1 Headphones
]

cursor.executemany('INSERT INTO orders (product_id, quantity, total) VALUES (?, ?, ?)', orders)

# Commit changes and close connection
conn.commit()
conn.close()

print("Database created and seeded successfully.")
