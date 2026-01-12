# 🚀 SoftDesk API - Guide d'installation et configuration

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-6.0-green)
![DRF](https://img.shields.io/badge/DRF-3.16-red)

API REST pour gérer des projets de développement collaboratifs avec système de suivi de problèmes (issues) et commentaires.

## 📋 Table des matières

- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Lancement](#-lancement)
- [Utilisation de l'API](#-utilisation-de-lapi)
- [Structure du projet](#-structure-du-projet)
- [Documentation](#-documentation)

---

## 🔧 Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Python 3.13** ou supérieur
- **pip** (gestionnaire de paquets Python)
- **Git** (pour cloner le projet)
- **PowerShell** (Windows) ou **Terminal** (Mac/Linux)

### Vérifier les installations

```powershell
python --version    # Doit afficher Python 3.13.x
pip --version       # Doit afficher pip 24.x ou supérieur
git --version       # Doit afficher git version 2.x
```

---

## 📥 Installation

### 1. Cloner le repository

```powershell
git clone https://github.com/votre-username/OC_SoftDesk.git
cd OC_SoftDesk
```

### 2. Créer un environnement virtuel

**Windows (PowerShell)** :
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Mac/Linux** :
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Vous devriez voir `(.venv)` apparaître dans votre terminal.

### 3. Installer les dépendances

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

**Dépendances principales** :
- Django 6.0
- djangorestframework 3.16.1
- djangorestframework-simplejwt 5.3.0+
- django-cors-headers 4.9.0+
- drf-nested-routers 0.95.0+

### 4. Créer le fichier requirements.txt (si nécessaire)

Si le fichier `requirements.txt` n'existe pas :

```powershell
pip install django==6.0
pip install djangorestframework==3.16.1
pip install djangorestframework-simplejwt
pip install django-cors-headers
pip install drf-nested-routers
pip freeze > requirements.txt
```

---

## ⚙️ Configuration

### 1. Variables d'environnement (optionnel)

Pour la production, créez un fichier `.env` à la racine :

```env
SECRET_KEY=votre-clé-secrète-django
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

**Note** : Pour le développement, les valeurs par défaut dans `settings.py` suffisent.

### 2. Configuration de la base de données

Le projet utilise **SQLite** par défaut (aucune configuration nécessaire).

Pour **PostgreSQL** en production, modifiez `core/settings.py` :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'softdesk_db',
        'USER': 'votre_user',
        'PASSWORD': 'votre_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3. Appliquer les migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

Cela crée les tables :
- `users_customuser` (utilisateurs)
- `projects_project` (projets)
- `projects_contributor` (contributeurs)
- `issues_issue` (problèmes)
- `issues_comment` (commentaires)

### 4. Créer un superutilisateur (admin)

```powershell
python manage.py createsuperuser
```

Suivez les instructions :
- Username : `admin`
- Email : `admin@example.com`
- Password : *(votre mot de passe)*
- Age : `30`
- can_be_contacted : `yes`
- can_data_be_shared : `yes`

### 5. (Optionnel) Charger des données de test

```powershell
python manage.py loaddata fixtures/initial_data.json
```

---

## 🚀 Lancement

### Démarrer le serveur de développement

```powershell
python manage.py runserver
```

Le serveur démarre sur **http://127.0.0.1:8000/**

Vous devriez voir :
```
Django version 6.0, using settings 'core.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Accéder à l'interface d'administration

Ouvrez votre navigateur : **http://127.0.0.1:8000/admin/**

Connectez-vous avec le superutilisateur créé précédemment.

### Tester l'API

L'API REST est accessible sur : **http://127.0.0.1:8000/api/**

---

## 📡 Utilisation de l'API

### 1. Créer un compte utilisateur

**Endpoint** : `POST /api/auth/register/`

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/register/" `
    -Method Post `
    -Body (@{
        username="alice"
        password="motdepasse123"
        email="alice@example.com"
        age=25
        can_be_contacted=$true
        can_data_be_shared=$true
    } | ConvertTo-Json) `
    -ContentType "application/json"
```

**Alternative avec cURL** :
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"motdepasse123","email":"alice@example.com","age":25}'
```

### 2. Se connecter et obtenir un token JWT

**Endpoint** : `POST /api/token/`

```powershell
$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/token/" `
    -Method Post `
    -Body (@{username="alice"; password="motdepasse123"} | ConvertTo-Json) `
    -ContentType "application/json"

$token = $response.access
Write-Host "Token: $token"
```

**Réponse** :
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 3. Utiliser le token pour accéder à l'API

**Exemple** : Créer un projet

```powershell
$headers = @{Authorization="Bearer $token"}

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/projects/" `
    -Method Post `
    -Headers $headers `
    -Body (@{
        name="Mon Projet API"
        description="Description du projet"
        type="backend"
    } | ConvertTo-Json) `
    -ContentType "application/json"
```

### 4. Endpoints disponibles

#### Authentification (sans token)
```
POST /api/auth/register/        # Inscription
POST /api/token/                # Login (obtenir token)
POST /api/token/refresh/        # Rafraîchir token
```

#### Utilisateurs (token requis)
```
GET    /api/auth/profile/       # Voir son profil
DELETE /api/auth/profile/       # Supprimer son compte (RGPD)
```

#### Projets (token requis)
```
GET    /api/projects/                     # Liste des projets (paginé)
POST   /api/projects/                     # Créer un projet
GET    /api/projects/{id}/                # Détail d'un projet
PUT    /api/projects/{id}/                # Modifier un projet (auteur)
DELETE /api/projects/{id}/                # Supprimer un projet (auteur)
GET    /api/projects/{id}/contributors/   # Liste des contributeurs
POST   /api/projects/{id}/contributors/   # Ajouter un contributeur (auteur)
DELETE /api/projects/{pid}/contributors/{cid}/  # Retirer un contributeur
```

#### Issues (token requis)
```
GET    /api/projects/{id}/issues/         # Liste des issues
POST   /api/projects/{id}/issues/         # Créer une issue
GET    /api/projects/{pid}/issues/{iid}/  # Détail d'une issue
PUT    /api/projects/{pid}/issues/{iid}/  # Modifier (auteur issue)
DELETE /api/projects/{pid}/issues/{iid}/  # Supprimer (auteur issue)
```

#### Commentaires (token requis)
```
GET    /api/projects/{p}/issues/{i}/comments/      # Liste
POST   /api/projects/{p}/issues/{i}/comments/      # Créer
GET    /api/projects/{p}/issues/{i}/comments/{c}/  # Détail
PUT    /api/projects/{p}/issues/{i}/comments/{c}/  # Modifier (auteur)
DELETE /api/projects/{p}/issues/{i}/comments/{c}/  # Supprimer (auteur)
```

### 5. Pagination

Toutes les listes sont paginées (10 éléments par page) :

```powershell
# Page 1
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/projects/" -Headers $headers

# Page 2
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/projects/?page=2" -Headers $headers
```

**Réponse paginée** :
```json
{
  "count": 42,
  "next": "http://127.0.0.1:8000/api/projects/?page=2",
  "previous": null,
  "results": [ /* 10 projets */ ]
}
```

---

## 📁 Structure du projet

```
OC_SoftDesk/
│
├── core/                      # Configuration Django
│   ├── __init__.py
│   ├── settings.py           # Configuration principale
│   ├── urls.py               # URLs racine
│   ├── wsgi.py
│   └── asgi.py
│
├── users/                     # App utilisateurs
│   ├── models.py             # CustomUser (RGPD)
│   ├── views.py              # Register, Profile, Delete
│   ├── serializers.py        # UserSerializer
│   ├── urls.py
│   └── permissions.py        # IsSelfUser
│
├── projects/                  # App projets
│   ├── models.py             # Project, Contributor
│   ├── views.py              # ProjectViewSet, ContributorViewSet
│   ├── serializers.py        # ProjectListSerializer, ProjectDetailSerializer
│   ├── permissions.py        # IsProjectAuthor, IsProjectContributor...
│   └── urls.py
│
├── issues/                    # App issues & commentaires
│   ├── models.py             # Issue, Comment
│   ├── views.py              # IssueViewSet, CommentViewSet
│   ├── serializers.py        # IssueListSerializer, IssueDetailSerializer
│   ├── permissions.py        # IsIssueAuthorOrReadOnly...
│   └── urls.py
│
├── db.sqlite3                 # Base de données (dev)
├── manage.py                  # Script de gestion Django
├── pyproject.toml             # Configuration Poetry
├── requirements.txt           # Dépendances pip
│
└── Documentation/
    ├── README.md              # Ce fichier
    ├── COMPTE_RENDU.md        # Explication complète
    ├── PERMISSIONS.md         # Système de permissions
    ├── OPTIMISATION.md        # Optimisations performance
    ├── REFACTORING.md         # Améliorations possibles
    └── CHECKLIST.md           # Validation exigences
```

---

## 🧪 Tests

### Lancer les tests Django

```powershell
python manage.py test
```

### Vérifier la couverture de code

```powershell
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Génère un rapport HTML dans htmlcov/
```

### Tests manuels avec Postman

1. Importer la collection Postman (si disponible)
2. Configurer la variable d'environnement `base_url` = `http://127.0.0.1:8000`
3. Configurer la variable `token` après le login
4. Exécuter les requêtes

---

## 🔒 Sécurité et RGPD

### Conformité RGPD implémentée

✅ **Consentement explicite** : Champs `can_be_contacted` et `can_data_be_shared`  
✅ **Protection mineurs** : `can_data_be_shared` forcé à `False` si âge < 15 ans  
✅ **Droit à l'oubli** : `DELETE /api/auth/profile/` supprime toutes les données (CASCADE)  
✅ **Confidentialité** : Les utilisateurs ne voient que leurs projets  
✅ **Suppression réelle** : Pas de soft-delete  

### JWT Token

- **Access token** : Valide 60 minutes
- **Refresh token** : Valide 10 jours
- **Header requis** : `Authorization: Bearer <token>`

### Permissions

- **Projet** : Seul l'auteur peut modifier/supprimer
- **Contributeur** : Seul l'auteur du projet peut ajouter/retirer
- **Issue** : Seul l'auteur de l'issue peut modifier/supprimer
- **Commentaire** : Seul l'auteur du commentaire peut modifier/supprimer

---

## 📄 Licence

Projet éducatif - OpenClassrooms 2026

---

## 👤 Auteur

**Noam**  
Formation : Développeur Python - OpenClassrooms  
Date : Janvier 2026

---

## 🎯 Technologies utilisées

- **Backend** : Django 6.0, Django REST Framework 3.16
- **Authentification** : djangorestframework-simplejwt (JWT)
- **Base de données** : SQLite (dev) / PostgreSQL (prod)
- **Routing** : drf-nested-routers
- **CORS** : django-cors-headers
- **Python** : 3.13

---

**Bon développement ! 🚀**
