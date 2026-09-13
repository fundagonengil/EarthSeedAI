import sqlite3

DATABASE = "earthseed.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Tablo yoksa otomatik oluşturur"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            telefon TEXT NOT NULL,
            mesaj TEXT,
            tarih DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def lead_ekle(isim, telefon, mesaj):
    init_db()  # Her kayıt öncesi tablonun varlığından emin oluyoruz
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO leads (isim, telefon, mesaj) VALUES (?, ?, ?)",
        (str(isim), str(telefon), str(mesaj))
    )
    conn.commit()
    conn.close()

def tum_leadler():
    init_db()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, isim, telefon, mesaj, tarih FROM leads ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]