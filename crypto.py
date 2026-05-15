from cryptography.fernet import Fernet

def generer_cle():
    return Fernet.generate_key().decode()

def chiffrer(texte, cle):
    try:
        f = Fernet(cle.encode())
        return f.encrypt(texte.encode()).decode()
    except:
        return "❌ Clé invalide"

def dechiffrer(texte_chiffre, cle):
    try:
        f = Fernet(cle.encode())
        return f.decrypt(texte_chiffre.encode()).decode()
    except:
        return "❌ Clé invalide ou texte incorrect"
    
    
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import base64

def generer_cles_rsa():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    priv = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()

    pub = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()

    with open('rsa_public.pem', 'w') as f:
        f.write(pub)
    with open('rsa_private.pem', 'w') as f:
        f.write(priv)

    return pub, priv

def chiffrer_rsa(texte, cle_publique):
    try:
        from cryptography.hazmat.primitives.serialization import load_pem_public_key
        pub_key = load_pem_public_key(cle_publique.encode())
        encrypted = pub_key.encrypt(
            texte.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(encrypted).decode()
    except Exception as e:
        return f"❌ Erreur : {str(e)}"

def dechiffrer_rsa(texte_chiffre, cle_privee):
    try:
        from cryptography.hazmat.primitives.serialization import load_pem_private_key
        priv_key = load_pem_private_key(cle_privee.encode(), password=None)
        decrypted = priv_key.decrypt(
            base64.b64decode(texte_chiffre),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted.decode('utf-8')
    except Exception as e:
        return f"❌ Erreur : {str(e)}"