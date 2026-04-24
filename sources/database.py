import binascii
import hashlib
import hmac
import os
import sqlite3
from pathlib import Path


# -----------------------------
# CONFIGURATION
# -----------------------------
DB_PATH = Path("databases/database.db")
HASH_NAME = "sha256"
ITERATIONS = 200_000
SALT_SIZE = 16  # bytes


# -----------------------------
# PASSWORD HASHING
# -----------------------------
def hash_password(password: str) -> str:
    salt = os.urandom(SALT_SIZE)
    dk = hashlib.pbkdf2_hmac(
        HASH_NAME,
        password.encode("utf-8"),
        salt,
        ITERATIONS
    )

    salt_hex = binascii.hexlify(salt).decode()
    dk_hex = binascii.hexlify(dk).decode()

    return (
        f"{HASH_NAME}$"
        f"{ITERATIONS}$"
        f"{salt_hex}$"
        f"{dk_hex}"
    )


def verify_password(stored: str, password: str) -> bool:
    hash_name, iters, salt_hex, dk_hex = stored.split("$")
    salt = binascii.unhexlify(salt_hex)
    expected = binascii.unhexlify(dk_hex)

    dk = hashlib.pbkdf2_hmac(
        hash_name,
        password.encode("utf-8"),
        salt,
        int(iters)
    )

    return hmac.compare_digest(dk, expected)


# -----------------------------
# DATABASE
# -----------------------------
def connect():
    return sqlite3.connect(DB_PATH)


def create():
    Path("databases").mkdir(exist_ok=True)

    if DB_PATH.exists():
        return

    with connect() as con:
        cur = con.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS goods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'user'
            )
        """)

        cur.executemany("""
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

        cur.executemany("""
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

    stored_hash = user[2]
    return verify_password(stored_hash, password)


def get_user(name: str):
    with connect() as con:
        cur = con.cursor()
        cur.execute("""SELECT id, name, password, role
        FROM users WHERE name = ?""", (name,))
        return cur.fetchone()


def load():
    with connect() as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM goods")
        return cur.fetchall()


def reduce_quantity(self, cart_list):
    with connect() as con:
        cur = con.cursor()
        for item in self.cart_list:
            cur.execute("""
                UPDATE goods
                SET quantity = quantity - ?
                WHERE id = ?
            """, (item["quantity"], item["id"]))


def retrieve_info(id: int):
    with connect() as con:
        cur = con.cursor()
        cur.execute("""
            SELECT name, price, quantity
            FROM goods
            WHERE id = ?
        """, (id,))
        return cur.fetchone()