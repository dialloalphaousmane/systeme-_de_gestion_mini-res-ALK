import os
import django
import sys
from django.contrib.auth.hashers import make_password

# Configure le chemin pour trouver votre projet Django
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SGM.settings')

# Initialise Django
django.setup()

from accounts.models import CustomUser

# --- Configuration des utilisateurs de test ---
# Chaque tuple contient: (username, email, password, role, first_name, last_name)
TEST_USERS = [
    ('admin_user', 'admin@example.com', 'Password123!', CustomUser.Role.ADMIN, 'Admin', 'User'),
    ('agent_minier', 'agent.minier@example.com', 'Password123!', CustomUser.Role.AGENT_MINIER, 'Agent', 'Minier'),
    ('resp_site', 'resp.site@example.com', 'Password123!', CustomUser.Role.RESPONSABLE_SITE, 'Responsable', 'Site'),
    ('chauffeur', 'chauffeur@example.com', 'Password123!', CustomUser.Role.CHAUFFEUR, 'Chauffeur', 'Transporteur'),
    ('douane', 'douane@example.com', 'Password123!', CustomUser.Role.DOUANE, 'Responsable', 'Douane'),
    ('environnement', 'env@example.com', 'Password123!', CustomUser.Role.ENVIRONNEMENT, 'Responsable', 'Environnement'),
    ('lecteur', 'lecteur@example.com', 'Password123!', CustomUser.Role.LECTEUR, 'Lecteur', 'Visiteur'),
]

def create_test_users():
    """Crée une série d'utilisateurs de test avec différents rôles."""
    print("--- Début de la création des utilisateurs de test ---")
    
    for username, email, password, role, first_name, last_name in TEST_USERS:
        # Vérifie si l'utilisateur existe déjà
        if CustomUser.objects.filter(username=username).exists():
            print(f"L'utilisateur '{username}' existe déjà. Ignoré.")
            continue

        # Crée le nouvel utilisateur
        try:
            user = CustomUser.objects.create(
                username=username,
                email=email,
                password=make_password(password),  # Hasher le mot de passe
                role=role,
                first_name=first_name,
                last_name=last_name,
                is_staff=True,  # Permet l'accès à l'admin si nécessaire
                is_active=True
            )
            print(f"Utilisateur '{username}' ({user.get_role_display()}) créé avec succès.")
        except Exception as e:
            print(f"Erreur lors de la création de l'utilisateur '{username}': {e}")

    print('\n--- Fin de la création des utilisateurs de test ---\n')

if __name__ == "__main__":
    create_test_users()