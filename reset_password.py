from auth import get_all_users, reset_password, init_users

init_users()

print("=" * 40)
print("   🔐 CYBERTOOLS - Reset Mot de Passe")
print("=" * 40)

users = get_all_users()
if not users:
    print("❌ Aucun utilisateur trouvé !")
else:
    print("\n📋 Utilisateurs existants :")
    for u in users:
        print(f"  [{u[0]}] {u[1]}")

    print()
    username = input("Entrez le nom d'utilisateur : ").strip()
    nouveau = input("Nouveau mot de passe : ").strip()
    confirmer = input("Confirmer le mot de passe : ").strip()

    if nouveau != confirmer:
        print("\n❌ Les mots de passe ne correspondent pas !")
    elif len(nouveau) < 6:
        print("\n❌ Mot de passe trop court (min 6 caractères) !")
    else:
        success, message = reset_password(username, nouveau)
        if success:
            print(f"\n✅ {message}")
        else:
            print(f"\n❌ {message}")

input("\nAppuyez sur Entrée pour quitter...")
