import os
import sqlite3

from pathlib import Path

from sources.config import BASE_DIR, DB_PATH
from sources.hashing import hash_password, verify_password


# -----------------------------
# DATABASE
# -----------------------------

def connect():
    return sqlite3.connect(DB_PATH)


def create():
    Path(os.path.join(BASE_DIR, "databases")).mkdir(exist_ok=True)

    if Path(DB_PATH).exists():
        return

    with connect() as con:
        cur = con.cursor()

        _ = cur.execute("""
            CREATE TABLE IF NOT EXISTS goods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
        """)

        _ = cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'user'
            )
        """)

        _ = cur.executemany("""
            INSERT INTO goods (name, price, quantity)
            VALUES (?, ?, ?)
        """, [
            ("Bugatti Bolide", 12.99, 100),
            ("Mazda MX-5", 2.99, 160),
            ("Nissan GT-R", 14.99, 40)
        ])

        users = [
            ("utilizador", hash_password("1234"), "user"),
            ("administrador", hash_password("A12B34c56!"), "admin")
        ]

        _ = cur.executemany("""
            INSERT INTO users (name, password, role)
            VALUES (?, ?, ?)
        """, users)


# -----------------------------
# QUERIES
# -----------------------------

def check_login(name: str, password: str) -> bool:
    user = get_user(name)

    if not user:
        return False

    stored_hash = user["password"]

    return verify_password(stored_hash, password)


def fetch_all():
    with connect() as con:
        cur = con.cursor()

        _ = cur.execute("SELECT id, name, price, quantity FROM goods")
        rows = cur.fetchall()

    return [
        {"id": r[0], "name": r[1], "price": r[2], "quantity": r[3]}
        for r in rows
    ]


def get_user(name: str):
    with connect() as con:
        cur = con.cursor()
        _ = cur.execute("""SELECT id, name, password, role
        FROM users WHERE name = ?""", (name,))
        row = cur.fetchone()

    if row is None:
        return None

    return {"id": row[0], "name": row[1], "password": row[2], "role": row[3]}


def reduce_quantity(cart_list):
    with connect() as con:
        cur = con.cursor()

        for item in cart_list:
            # Ensure quantity will not go negative
            _ = cur.execute("""
                UPDATE goods
                SET quantity = quantity - ?
                WHERE id = ?
            """, (item["quantity"], item["id"]))


def retrieve_info(id: int):
    with connect() as con:
        cur = con.cursor()
        _ = cur.execute(
            "SELECT id, name, price, quantity FROM goods WHERE id = ?",
            (id,),
        )
        r = cur.fetchone()

    if r is None:
        return None

    return {"id": r[0], "name": r[1], "price": r[2], "quantity": r[3]}