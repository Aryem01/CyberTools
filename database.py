import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('historique.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS historique (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            details TEXT,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def ajouter_action(action, details):
    conn = sqlite3.connect('historique.db')
    c = conn.cursor()
    c.execute(
        'INSERT INTO historique (action, details, date) VALUES (?, ?, ?)',
        (action, details, datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    )
    conn.commit()
    conn.close()

def get_historique():
    conn = sqlite3.connect('historique.db')
    c = conn.cursor()
    c.execute('SELECT * FROM historique ORDER BY id DESC LIMIT 50')
    rows = c.fetchall()
    conn.close()
    return rows

def vider_historique():
    conn = sqlite3.connect('historique.db')
    c = conn.cursor()
    c.execute('DELETE FROM historique')
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect('historique.db')
    c = conn.cursor()

    c.execute('SELECT COUNT(*) FROM historique')
    total = c.fetchone()[0]

    c.execute('''SELECT action, COUNT(*) as nb
                 FROM historique
                 GROUP BY action
                 ORDER BY nb DESC''')
    par_action = c.fetchall()

    today = datetime.now().strftime('%d/%m/%Y')
    c.execute("SELECT COUNT(*) FROM historique WHERE date LIKE ?", (f'{today}%',))
    aujourd_hui = c.fetchone()[0]

    c.execute('SELECT action, date FROM historique ORDER BY id DESC LIMIT 1')
    derniere = c.fetchone()

    conn.close()
    return {
        'total': total,
        'par_action': par_action,
        'aujourd_hui': aujourd_hui,
        'derniere': derniere
    }