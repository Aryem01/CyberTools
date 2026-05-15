# 🔐 CyberTools

Application web de cybersécurité construite avec Python et Flask.

🌐 **Demo en ligne** : https://cybertools-o68i.onrender.com

---

## ✨ Fonctionnalités

- 🔑 **Générateur de mots de passe** — longueur et options personnalisables
- 🔍 **Vérificateur de force** — analyse la solidité d'un mot de passe
- 🔒 **Chiffrement AES** — chiffre et déchiffre des messages avec une clé Fernet
- 🔐 **Chiffrement RSA** — chiffrement asymétrique avec clé publique/privée
- 🌐 **Scanner de ports** — détecte les ports ouverts sur une adresse IP
- 📊 **Dashboard** — statistiques et graphiques des actions
- 📋 **Historique** — sauvegarde de toutes les actions
- 👤 **Authentification** — login, register, reset mot de passe

---

##  Technologies utilisées

| Technologie | Utilisation |
|---|---|
| Python 3 | Langage principal |
| Flask | Framework web |
| SQLite / PostgreSQL | Base de données |
| Cryptography | Chiffrement AES |
| RSA | Chiffrement RSA |
| Chart.js | Graphiques dashboard |
| Render.com | Hébergement |

---

##  Installation locale

**1. Cloner le projet**
```bash
git clone https://github.com/Aryem01/CyberTools.git
cd CyberTools
```

**2. Installer les dépendances**
```bash
pip install -r requirements.txt
```

**3. Lancer l'application**
```bash
python app.py
```

**4. Ouvrir dans le navigateur**
```
http://127.0.0.1:5000
```

---

##  Structure du projet

```
cyber-tools/
├── app.py              # Application Flask principale
├── auth.py             # Authentification (login, register, reset)
├── crypto.py           # Chiffrement AES et RSA
├── database.py         # Base de données (SQLite / PostgreSQL)
├── port_scanner.py     # Scanner de ports TCP
├── requirements.txt    # Dépendances Python
├── Procfile            # Configuration Render
├── templates/
│   ├── index.html      # Page principale
│   └── login.html      # Page de connexion
└── static/
    └── style.css       # Styles CSS
```

---

## 🔒 Sécurité

- Mots de passe hashés avec **PBKDF2-SHA256** + salt
- Chiffrement **AES-128 (Fernet)** pour les messages
- Chiffrement **RSA 2048 bits** avec padding OAEP
- Sessions Flask sécurisées
- Fichiers sensibles exclus du repository (.pem, .db)

---

##  Aperçu

| Dashboard | Chiffrement | Scanner |
|---|---|---|
| Graphiques des actions | AES + RSA | Ports TCP ouverts |

---

##  Auteur

**Aryem** — Étudiant en Master Cybersécurité

---

##  Licence

Ce projet est open source — libre d'utilisation à des fins éducatives.
