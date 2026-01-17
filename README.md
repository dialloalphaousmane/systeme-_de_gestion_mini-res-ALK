# SGM - Système de Gestion Minière

## 📋 Description

SGM est une plateforme complète de gestion des miniére premières et de logistique minière. Elle permet de suivre les extractions, gérer les transports, contrôler les exports et monitorer l'impact environnemental.

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.10+
- Django 5.2+
- Node.js (pour le développement frontend)

### Installation
```bash
# Cloner le projet
git clone <repository-url>
cd SGM

# Activer l'environnement virtuel
venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate   # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Démarrer le serveur
python manage.py runserver
```

## 🔗 URLs Disponibles

### 🏠 Pages Principales
- **Accueil** : `http://127.0.0.1:8000/`
- **Contact** : `http://127.0.0.1:8000/contact/`
- **Admin Django** : `http://127.0.0.1:8000/admin/`

### 🔐 Authentification
- **Connexion** : `http://127.0.0.1:8000/login/`
- **Déconnexion** : `http://127.0.0.1:8000/logout/`
- **Redirection tableau de bord** : `http://127.0.0.1:8000/dashboard/`

### 📊 Tableaux de Bord par Rôle
- **Admin** : `http://127.0.0.1:8000/dashboard/admin/`
- **Agent Minier** : `http://127.0.0.1:8000/dashboard/agent/`
- **Responsable de Site** : `http://127.0.0.1:8000/dashboard/site-manager/`
- **Chauffeur** : `http://127.0.0.1:8000/dashboard/driver/`
- **Douane** : `http://127.0.0.1:8000/dashboard/customs/`
- **Environnement** : `http://127.0.0.1:8000/dashboard/environment/`
- **Visualisateur** : `http://127.0.0.1:8000/dashboard/viewer/`

## 🔌 API Endpoints

### Authentification JWT
- **Token** : `http://127.0.0.1:8000/api/token/`
- **Refresh Token** : `http://127.0.0.1:8000/api/token/refresh/`

### APIs par Module
- **Comptes** : `http://127.0.0.1:8000/api/accounts/`
- **Sites** : `http://127.0.0.1:8000/api/sites/`
- **Extractions** : `http://127.0.0.1:8000/api/extraction/`
- **Transports** : `http://127.0.0.1:8000/api/transport/`
- **Exports** : `http://127.0.0.1:8000/api/export/`
- **Environnement** : `http://127.0.0.1:8000/api/environment/`
- **Notifications** : `http://127.0.0.1:8000/api/notifications/`
- **Dashboard (API)** : `http://127.0.0.1:8000/api/dashboard/`

### Notes
- **Pages Dashboard (HTML)** : commencent par `http://127.0.0.1:8000/dashboard/` (ex: `/dashboard/viewer/`).
- **Dashboard API (JSON)** : commence par `http://127.0.0.1:8000/api/dashboard/` (ex: `/api/dashboard/metrics/`, `/api/dashboard/reports/`).

## 👥 Rôles et Permissions

### Rôles Disponibles
1. **`admin`** - Accès complet à toutes les fonctionnalités
2. **`agent_minier`** - Gestion des extractions et sites
3. **`responsable_site`** - Supervision des opérations sur site
4. **`chauffeur`** - Gestion des transports assignés
5. **`douane`** - Contrôle des exports et documents
6. **`environnement`** - Suivi environnemental et rapports
7. **`viewer`** - Accès en lecture seule aux données

### Flux de Navigation
1. **Non connecté** → `/dashboard/` → redirige vers `/login/`
2. **Connexion réussie** → redirection selon le rôle
3. **Déconnexion** → retour à l'accueil

## 🏗️ Structure du Projet

```
SGM/
├── SGM/                    # Configuration principale
│   ├── settings.py         # Paramètres Django
│   ├── urls.py            # URLs principales
│   └── wsgi.py            # Configuration WSGI
├── accounts/               # Gestion des utilisateurs
├── dashboard/              # Tableaux de bord
│   ├── views.py           # Vues principales
│   ├── views_dashboard.py  # Vues des tableaux de bord
│   └── urls.py            # URLs des tableaux de bord
├── sites/                  # Gestion des sites
├── extraction/             # Gestion des extractions
├── transport/              # Gestion des transports
├── export/                 # Gestion des exports
├── environment/            # Suivi environnemental
├── notifications/          # Système de notifications
├── templates/              # Templates HTML
│   ├── base.html          # Template de base
│   ├── home.html          # Page d'accueil
│   └── login.html         # Page de connexion
└── static/                 # Fichiers statiques
    ├── css/
    ├── js/
    └── images/
```

## 🛠️ Technologies Utilisées

### Backend
- **Django 5.2** - Framework web
- **Django REST Framework** - API REST
- **JWT Authentication** - Authentification par token
- **PostgreSQL** - Base de données (configurable)

### Frontend
- **Tailwind CSS** - Framework CSS
- **Font Awesome** - Icônes
- **JavaScript Vanilla** - Interactivité

### Développement
- **Python 3.10+**
- **Pip** - Gestion des dépendances
- **Virtual Environment** - Isolation

## 📝 Fonctionnalités Implémentées

### ✅ Authentification
- Page de connexion moderne et responsive
- Validation en temps réel des champs
- Messages d'erreur/succès
- Option "Se souvenir de moi"
- Redirection automatique selon le rôle
- Support pour next_url (redirection après connexion)

### ✅ Tableaux de Bord
- Interface par rôle personnalisée
- Statistiques en temps réel
- Widgets configurables
- Rapports et analyses

### ✅ Gestion des Données
- CRUD complet pour toutes les entités
- API REST pour l'intégration mobile/web
- Validation des données
- Historique des modifications

### ✅ Notifications
- Système de notifications en temps réel
- Email notifications
- Alertes personnalisées

## 🔧 Configuration

### Variables d'Environnement
```bash
# Base de données
DATABASE_URL=postgresql://user:password@localhost:sgm_db

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Sécurité
SECRET_KEY=votre-secret-key-ici
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com
```

### Fichiers Statiques
```bash
# Collecter les fichiers statiques
python manage.py collectstatic

# Servir les fichiers média en développement
python manage.py runserver --settings=SGM.settings_development
```

## 🧪 Tests

### Lancer les tests
```bash
# Tests unitaires
python manage.py test

# Tests avec couverture
coverage run --source='.' manage.py test
coverage report
```

### Tests API
```bash
# Tests des endpoints API
python manage.py test api.tests

# Tests d'authentification
python manage.py test accounts.tests
```

## 📚 Documentation

### API Documentation
- **Swagger UI** : `http://127.0.0.1:8000/api/doc/`
- **ReDoc** : `http://127.0.0.1:8000/api/redoc/`

### Guides
- [Guide d'installation](docs/installation.md)
- [Guide des rôles](docs/roles.md)
- [Guide API](docs/api.md)
- [Guide de déploiement](docs/deployment.md)

## 🚨 Dépannage

### Problèmes Communs

#### Erreur de migration
```bash
# Réinitialiser les migrations
python manage.py migrate --fake-initial
```

#### Problème de fichiers statiques
```bash
# Recollecter les fichiers statiques
python manage.py collectstatic --noinput
```

#### Erreur de connexion
- Vérifier que le serveur est démarré
- Confirmer les URLs dans `SGM/urls.py`
- Vérifier les permissions des rôles

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour les détails.

## 👥 Équipe

- **Développeur Principal** : [Votre Nom]
- **Chef de Projet** : [Nom du Chef]
- **Designer UI/UX** : [Nom du Designer]

## 📞 Support

- **Email** : support@sgm-example.com
- **Téléphone** : +1 (555) 123-4567
- **Documentation** : [Wiki du projet](https://github.com/votre-repo/sgm/wiki)

---

pour la connexion avec les role 
------------------------------------------------------------------------     
admin_user     | admin@example.com         | Administrateur
agent_minier   | agent.minier@example.com  | Agent Minier
alpha          | alpha@sgm.local           | Lecteur/Visiteur
chauffeur      | chauffeur@example.com     | Chauffeur/Transporteur
douane         | douane@example.com        | Responsable Douane
environnement  | env@example.com           | Responsable Environnement       
lecteur        | lecteur@example.com       | Lecteur/Visiteur
resp_site      | resp.site@example.com     | Responsable Site




**© 2024 SGM - Système de Gestion Minière. Tous droits réservés.**
# systeme-_de_gestion_mini-res-ALK
