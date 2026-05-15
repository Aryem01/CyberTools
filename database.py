import os
import psycopg2
from datetime import datetime

DATABASE_URL = os.environ.get('DATABASE_URL')

def get_conn():
    if DATABASE_URL:
        return psycopg2.connect(DATABASE_URL)
    else:
        import sqlite3
        return sqlite3.connect('historique.db')

def is_postgres():
    return DATABASE_URL is not None

def init_db():
    conn = get_conn()
    c = conn.cursor()
    if is_postgres():
        c.execute('''
            CREATE TABLE IF NOT EXISTS historique (
                id SERIAL PRIMARY KEY,
                action TEXT NOT NULL,
                details TEXT,
                date TEXT NOT NULL
            )
        ''')
    else:
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
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        'INSERT INTO historique (action, details, date) VALUES (%s, %s, %s)' if is_postgres()
        else 'INSERT INTO historique (action, details, date) VALUES (?, ?, ?)',
        (action, details, datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    )
    conn.commit()
    conn.close()

def get_historique():
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM historique ORDER BY id DESC LIMIT 50')
    rows = c.fetchall()
    conn.close()
    return rows

def vider_historique():
    conn = get_conn()
    c = conn.cursor()
    c.execute('DELETE FROM historique')
    conn.commit()
    conn.close()

def get_stats():
    conn = get_conn()
    c = conn.cursor()

    c.execute('SELECT COUNT(*) FROM historique')
    total = c.fetchone()[0]

    c.execute('''SELECT action, COUNT(*) as nb
                 FROM historique
                 GROUP BY action
                 ORDER BY nb DESC''')
    par_action = c.fetchall()

    today = datetime.now().strftime('%d/%m/%Y')
    c.execute("SELECT COUNT(*) FROM historique WHERE date LIKE %s" if is_postgres()
              else "SELECT COUNT(*) FROM historique WHERE date LIKE ?",
              (f'{today}%',))
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