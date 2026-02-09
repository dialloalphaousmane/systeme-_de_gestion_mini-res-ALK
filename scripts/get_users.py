import os
import django
import sys

# Configure le chemin pour trouver votre projet Django
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SGM.settings')

# Initialise Django
django.setup()

from accounts.models import CustomUser

def list_users_with_roles():
    """Affiche la liste des utilisateurs avec leur nom d'utilisateur, email et rôle."""
    print("--- Liste des utilisateurs et de leurs rôles ---")
    
    users = CustomUser.objects.all().order_by('username')
    
    if not users.exists():
        print("Aucun utilisateur trouvé dans la base de données.")
        return

    # Détermine la largeur des colonnes pour un affichage propre
    max_username = max(len(u.username) for u in users) + 2
    max_email = max(len(u.email) for u in users) + 2
    max_role = max(len(u.get_role_display()) for u in users) + 2

    # En-tête du tableau
    header = f"{'UTILISATEUR'.ljust(max_username)}| {'EMAIL'.ljust(max_email)}| {'RÔLE'.ljust(max_role)}"
    print(header)
    print('-' * len(header))

    # Affiche chaque utilisateur
    for user in users:
        username = user.username.ljust(max_username)
        email = user.email.ljust(max_email)
        role = user.get_role_display().ljust(max_role)
        print(f"{username}| {email}| {role}")

    print('\n--- Fin de la liste ---\n')

if __name__ == "__main__":
    list_users_with_roles()