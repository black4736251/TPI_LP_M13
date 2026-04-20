import sqlite3
from pathlib import Path

def connect():
    con = sqlite3.connect("databases/database.db")
    cur = con.cursor()
    return con, cur

def create():
    if Path("databases/database.db").exists():
        return
    con, cur = connect()
    cur.execute('''CREATE TABLE IF NOT EXISTS goods
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT,
                    price DOUBLE NOT NULL, quantity INTEGER NOT NULL)''')
    cur.execute('''INSERT INTO goods (name, price, quantity) VALUES
                    ('Bugatti Bolide','12.99','100'),
                    ('Mazda MX-5','2.99','160'),
                    ('Nissan GT-R','14.99','40')''')
    con.commit()
    cur.close()
    con.close()

def load():
    con, cur = connect()
    result = cur.execute("SELECT * FROM goods")
    if result:
        database = cur.fetchall()
    else:
        database = []
    cur.close()
    con.close()
    return database

def retrieve_info(id: int):
    con, cur = connect()
    cur.execute('''SELECT name, price, quantity FROM goods
    WHERE id = ?''', (id,))
    result = cur.fetchone()
    con.close()
    if result is None:
        return None
    name, price, quantity = result
    return name, price, quantity

def reduce_quantity(self):
    con, cur = connect()
    for item in self.cart_list:
        cur.execute('''UPDATE goods SET quantity = quantity - ?
        WHERE id = ?''', (item['quantity'], item['id']))
    con.commit()
    cur.close()
    con.close()