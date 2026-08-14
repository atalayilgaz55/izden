import sqlite3

from flask import current_app


def get_db():
    """
    SQLite veritabanına bağlanır.

    Flask uygulamasının ayarlarından veritabanı dosyasının
    yolunu alır ve bağlantıyı döndürür.
    """
    database_url = current_app.config["DATABASE_URL"]

    connection = sqlite3.connect(database_url)

    # Sonuçlara sütun isimleriyle erişebilmemizi sağlar.
    connection.row_factory = sqlite3.Row

    return connection


def init_db():
    """
    Veritabanını hazırlar.

    leads tablosu yoksa oluşturur.
    """
    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            telefon TEXT NOT NULL,
            mesaj TEXT,
            tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    db.commit()
    db.close()


def lead_ekle(isim, telefon, mesaj):
    """
    Yeni bir katılımcı kaydı oluşturur.
    """
    db = get_db()

    db.execute(
        """
        INSERT INTO leads (isim, telefon, mesaj)
        VALUES (?, ?, ?)
        """,
        (isim, telefon, mesaj)
    )

    db.commit()
    db.close()


def tum_leadler():
    """
    Veritabanındaki tüm katılımcıları
    en yeniden en eskiye doğru getirir.
    """
    db = get_db()

    leads = db.execute(
        """
        SELECT id, isim, telefon, mesaj, tarih
        FROM leads
        ORDER BY tarih DESC
        """
    ).fetchall()

    db.close()

    return leads