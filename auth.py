import sqlite3
import hashlib
import os

def init_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
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
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute(
            'INSERT INTO users (username, password, salt) VALUES (?, ?, ?)',
            (username, hashed, salt)
        )
        conn.commit()
        conn.close()
        return True, "Compte créé avec succès !"
    except sqlite3.IntegrityError:
        return False, "Ce nom d'utilisateur existe déjà"

def verifier_login(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT password, salt FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    if not user:
        return False, "Utilisateur introuvable"
    hashed, _ = hash_password(password, user[1])
    if hashed == user[0]:
        return True, "Connexion réussie !"
    return False, "Mot de passe incorrect"

def user_existe():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM users')
    count = c.fetchone()[0]
    conn.close()
    return count > 0

def reset_password(username, nouveau_password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    if not user:
        conn.close()
        return False, "Utilisateur introuvable"
    hashed, salt = hash_password(nouveau_password)
    c.execute(
        'UPDATE users SET password = ?, salt = ? WHERE username = ?',
        (hashed, salt, username)
    )
    conn.commit()
    conn.close()
    return True, "Mot de passe réinitialisé !"

def get_all_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT id, username FROM users')
    users = c.fetchall()
    conn.close()
    return users