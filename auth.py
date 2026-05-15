import os
import hashlib

DATABASE_URL = os.environ.get('DATABASE_URL')

def get_conn():
    if DATABASE_URL:
        import psycopg2
        return psycopg2.connect(DATABASE_URL)
    else:
        import sqlite3
        return sqlite3.connect('users.db')

def is_postgres():
    return DATABASE_URL is not None

def placeholder():
    return '%s' if is_postgres() else '?'

def init_users():
    conn = get_conn()
    c = conn.cursor()
    if is_postgres():
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                salt TEXT NOT NULL
            )
        ''')
    else:
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                salt TEXT NOT NULL
            )
        ''')
    conn.commit()
    conn.close()

def hash_password(password, salt=None):
    import os
    if salt is None:
        salt = os.urandom(32).hex()
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt.encode(),
        100000
    ).hex()
    return hashed, salt

def creer_compte(username, password):
    try:
        hashed, salt = hash_password(password)
        conn = get_conn()
        c = conn.cursor()
        p = placeholder()
        c.execute(
            f'INSERT INTO users (username, password, salt) VALUES ({p}, {p}, {p})',
            (username, hashed, salt)
        )
        conn.commit()
        conn.close()
        return True, "Compte créé avec succès !"
    except Exception as e:
        if 'unique' in str(e).lower() or 'duplicate' in str(e).lower():
            return False, "Ce nom d'utilisateur existe déjà"
        return False, str(e)

def verifier_login(username, password):
    conn = get_conn()
    c = conn.cursor()
    p = placeholder()
    c.execute(f'SELECT password, salt FROM users WHERE username = {p}', (username,))
    user = c.fetchone()
    conn.close()
    if not user:
        return False, "Utilisateur introuvable"
    hashed, _ = hash_password(password, user[1])
    if hashed == user[0]:
        return True, "Connexion réussie !"
    return False, "Mot de passe incorrect"

def reset_password(username, nouveau_password):
    conn = get_conn()
    c = conn.cursor()
    p = placeholder()
    c.execute(f'SELECT id FROM users WHERE username = {p}', (username,))
    user = c.fetchone()
    if not user:
        conn.close()
        return False, "Utilisateur introuvable"
    hashed, salt = hash_password(nouveau_password)
    c.execute(
        f'UPDATE users SET password = {p}, salt = {p} WHERE username = {p}',
        (hashed, salt, username)
    )
    conn.commit()
    conn.close()
    return True, "Mot de passe réinitialisé !"

def get_all_users():
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT id, username FROM users')
    users = c.fetchall()
    conn.close()
    return users

def user_existe():
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM users')
    count = c.fetchone()[0]
    conn.close()
    return count > 0