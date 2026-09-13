import sqlite3
from flask import current_app


def get_db():
    database_url = current_app.config["DATABASE_URL"]

    connection = sqlite3.connect(database_url)
    connection.row_factory = sqlite3.Row

    return connection


def init_db():
    connection = get_db()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                eposta TEXT,
        

                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()

    finally:
        connection.close()


def lead_ekle(isim, telefon, mesaj, eposta):
    connection = get_db()

    try:
        connection.execute(
            """
            INSERT INTO leads (isim, telefon, mesaj, eposta)
            VALUES (?, ?, ?, ?)
            """,
            (isim, telefon, mesaj, eposta )
        )

        connection.commit()

    finally:
        connection.close()


def tum_leadler():
    connection = get_db()

    try:
        leads = connection.execute(
            """
            SELECT id, isim, telefon, mesaj, tarih, eposta
            FROM leads
            ORDER BY tarih DESC
            """
        ).fetchall()

        return leads

    finally:
        connection.close()
        