import sqlite3

DATABASE = "earthseed.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Dict gibi erişim sağlamak için şart!
    return conn

def lead_ekle(isim, telefon, mesaj):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO leads (isim, telefon, mesaj) VALUES (?, ?, ?)",
        (str(isim), str(telefon), str(mesaj))
    )
    conn.commit()
    conn.close()

def tum_leadler():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, isim, telefon, mesaj, tarih FROM leads ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    # sqlite3.Row objesini standart dict'e çeviriyoruz
    return [dict(row) for row in rows]