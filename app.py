from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import random
import string
from crypto import generer_cle, chiffrer, dechiffrer
from port_scanner import scanner_ports
from database import init_db, ajouter_action, get_historique, vider_historique, get_stats
from auth import init_users, creer_compte, verifier_login, reset_password
from crypto import generer_cle, chiffrer, dechiffrer, generer_cles_rsa, chiffrer_rsa, dechiffrer_rsa

app = Flask(__name__)
app.secret_key = 'cybertools_secret_2024'
init_db()
init_users()

def generer_password(longueur, majuscules, chiffres, symboles):
    caracteres = string.ascii_lowercase
    if majuscules:
        caracteres += string.ascii_uppercase
    if chiffres:
        caracteres += string.digits
    if symboles:
        caracteres += string.punctuation
    return ''.join(random.choice(caracteres) for _ in range(longueur))

def verifier_force(mdp):
    force = 0
    conseil = []
    if len(mdp) >= 8:
        force += 1
    else:
        conseil.append("Utilise au moins 8 caractères")
    if any(c.isupper() for c in mdp):
        force += 1
    else:
        conseil.append("Ajoute des majuscules")
    if any(c.isdigit() for c in mdp):
        force += 1
    else:
        conseil.append("Ajoute des chiffres")
    if any(c in string.punctuation for c in mdp):
        force += 1
    else:
        conseil.append("Ajoute des symboles (!@#...)")
    if force == 4:
        return "💪 Très fort", "Excellent mot de passe !"
    elif force == 3:
        return "👍 Fort", " • ".join(conseil)
    elif force == 2:
        return "⚠️ Moyen", " • ".join(conseil)
    else:
        return "❌ Faible", " • ".join(conseil)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def get_context(active_tab='dashboard', **kwargs):
    kwargs['historique'] = get_historique()
    kwargs['stats'] = get_stats()
    kwargs['active_tab'] = active_tab
    kwargs['username'] = session.get('username')
    return kwargs

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if action == 'register':
            success, message = creer_compte(username, password)
            if success:
                session['username'] = username
                return redirect(url_for('home'))
            return render_template('login.html', message=message, success=False, action='register')
        elif action == 'reset':
            confirm = request.form.get('confirm', '')
            if password != confirm:
                return render_template('login.html', message="Les mots de passe ne correspondent pas !", success=False, action='reset')
            if len(password) < 6:
                return render_template('login.html', message="Mot de passe trop court (min 6) !", success=False, action='reset')
            success, message = reset_password(username, password)
            return render_template('login.html', message=message, success=success, action='reset')
        else:
            success, message = verifier_login(username, password)
            if success:
                session['username'] = username
                return redirect(url_for('home'))
            return render_template('login.html', message=message, success=False, action='login')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    return render_template('index.html', **get_context(active_tab='dashboard'))

@app.route('/generer', methods=['POST'])
@login_required
def generer():
    longueur = int(request.form.get('longueur', 12))
    majuscules = 'majuscules' in request.form
    chiffres = 'chiffres' in request.form
    symboles = 'symboles' in request.form
    password = generer_password(longueur, majuscules, chiffres, symboles)
    ajouter_action('🔑 Mot de passe généré', f'Longueur: {longueur}')
    return render_template('index.html', **get_context(active_tab='password', password=password))

@app.route('/verifier', methods=['POST'])
@login_required
def verifier():
    mdp = request.form.get('mdp', '')
    force, conseil = verifier_force(mdp)
    ajouter_action('🔍 Mot de passe vérifié', f'Force: {force}')
    return render_template('index.html', **get_context(active_tab='password', force=force, conseil=conseil))

@app.route('/generer-cle', methods=['POST'])
@login_required
def route_generer_cle():
    cle = generer_cle()
    with open('ma_cle.txt', 'w') as f:
        f.write(cle)
    ajouter_action('🔑 Clé AES générée', 'Clé sauvegardée dans ma_cle.txt')
    return render_template('index.html', **get_context(active_tab='crypto', cle=cle))

@app.route('/chiffrer', methods=['POST'])
@login_required
def route_chiffrer():
    texte = request.form.get('texte', '')
    auto_cle = 'auto_cle' in request.form
    cle = request.form.get('cle', '').strip()
    if auto_cle or not cle:
        cle = generer_cle()
        with open('ma_cle.txt', 'w') as f:
            f.write(cle)
    resultat = chiffrer(texte, cle)
    ajouter_action('🔒 Texte chiffré', f'Longueur texte: {len(texte)} caractères')
    return render_template('index.html', **get_context(active_tab='crypto', texte_chiffre=resultat, cle_utilisee=cle))

@app.route('/dechiffrer', methods=['POST'])
@login_required
def route_dechiffrer():
    texte_chiffre = request.form.get('texte_chiffre', '').strip()
    cle = request.form.get('cle', '').strip()
    texte_dechiffre = dechiffrer(texte_chiffre, cle)
    ajouter_action('🔓 Texte déchiffré', f'Résultat: {texte_dechiffre[:20]}...' if len(texte_dechiffre) > 20 else f'Résultat: {texte_dechiffre}')
    return render_template('index.html', **get_context(active_tab='crypto', texte_dechiffre=texte_dechiffre))

@app.route('/scanner', methods=['POST'])
@login_required
def route_scanner():
    ip = request.form.get('ip', '').strip()
    port_debut = int(request.form.get('port_debut') or 1)
    port_fin = int(request.form.get('port_fin') or 100)
    if port_fin - port_debut > 500:
        port_fin = port_debut + 500
    ports = scanner_ports(ip, port_debut, port_fin)
    ajouter_action('🌐 Scan de ports', f'IP: {ip} | Ports: {port_debut}-{port_fin} | Ouverts: {len(ports)}')
    return jsonify({'ports': ports, 'ip': ip})

@app.route('/vider-historique', methods=['POST'])
@login_required
def route_vider():
    vider_historique()
    return render_template('index.html', **get_context(active_tab='historique'))

@app.route('/generer-cles-rsa', methods=['POST'])
@login_required
def route_generer_cles_rsa():
    pub, priv = generer_cles_rsa()
    session['rsa_pub'] = pub
    session['rsa_priv'] = priv
    ajouter_action('🔐 Clés RSA générées', 'Clés sauvegardées dans rsa_public.pem et rsa_private.pem')
    return render_template('index.html', **get_context(active_tab='crypto', rsa_pub=pub, rsa_priv=priv))

@app.route('/chiffrer-rsa', methods=['POST'])
@login_required
def route_chiffrer_rsa():
    texte = request.form.get('texte_rsa', '')
    cle_pub = request.form.get('cle_pub_rsa', '').strip()
    resultat = chiffrer_rsa(texte, cle_pub)
    session['rsa_chiffre'] = resultat
    ajouter_action('🔐 Texte chiffré RSA', f'Longueur: {len(texte)} caractères')
    return render_template('index.html', **get_context(
        active_tab='crypto',
        rsa_chiffre=resultat,
        rsa_pub=session.get('rsa_pub'),
        rsa_priv=session.get('rsa_priv')
    ))

@app.route('/dechiffrer-rsa', methods=['POST'])
@login_required
def route_dechiffrer_rsa():
    texte_chiffre = request.form.get('texte_chiffre_rsa', '').strip()
    cle_priv = request.form.get('cle_priv_rsa', '').strip()
    resultat = dechiffrer_rsa(texte_chiffre, cle_priv)
    ajouter_action('🔓 Texte déchiffré RSA', f'Résultat: {resultat[:20]}...' if len(resultat) > 20 else f'Résultat: {resultat}')
    return render_template('index.html', **get_context(
        active_tab='crypto',
        rsa_dechiffre=resultat,
        rsa_pub=session.get('rsa_pub'),
        rsa_priv=session.get('rsa_priv'),
        rsa_chiffre=session.get('rsa_chiffre')
    ))
@app.route('/clear-rsa', methods=['POST'])
@login_required
def clear_rsa():
    session.pop('rsa_pub', None)
    session.pop('rsa_priv', None)
    session.pop('rsa_chiffre', None)
    return render_template('index.html', **get_context(active_tab='crypto'))  

if __name__ == '__main__':
    app.run(debug=True)