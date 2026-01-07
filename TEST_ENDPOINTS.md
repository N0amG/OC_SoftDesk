# Guide de Test des Endpoints Issues et Comments

## Étapes de Configuration

### 1. Créer et appliquer les migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Démarrer le serveur

```bash
python manage.py runserver
```

### 3. Obtenir un token JWT

Créez un utilisateur ou connectez-vous pour obtenir un token :

```bash
POST http://localhost:8000/api/token/
{
    "username": "votre_username",
    "password": "votre_password"
}
```

Réponse :
```json
{
    "access": "votre_access_token",
    "refresh": "votre_refresh_token"
}
```

## Endpoints Issues

### Lister les issues d'un projet

```
GET /api/projects/{project_id}/issues/
Authorization: Bearer {access_token}
```

### Créer une issue

```
POST /api/projects/{project_id}/issues/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "title": "Bug dans la connexion",
    "description": "Les utilisateurs ne peuvent pas se connecter",
    "priority": "high",
    "status": "to_do",
    "tag": "bug",
    "assignee_id": 2
}
```

**Champs disponibles :**
- `title` (obligatoire) : Titre de l'issue
- `description` (obligatoire) : Description détaillée
- `priority` : "low", "medium" (par défaut), "high"
- `status` : "to_do" (par défaut), "in_progress", "finished"
- `tag` : "bug", "feature", "task" (par défaut)
- `assignee_id` (optionnel) : ID d'un contributeur du projet

### Voir le détail d'une issue

```
GET /api/projects/{project_id}/issues/{issue_id}/
Authorization: Bearer {access_token}
```

### Modifier une issue (auteur uniquement)

```
PATCH /api/projects/{project_id}/issues/{issue_id}/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "status": "in_progress",
    "assignee_id": 3
}
```

### Supprimer une issue (auteur uniquement)

```
DELETE /api/projects/{project_id}/issues/{issue_id}/
Authorization: Bearer {access_token}
```

## Endpoints Comments

### Lister les commentaires d'une issue

```
GET /api/projects/{project_id}/issues/{issue_id}/comments/
Authorization: Bearer {access_token}
```

### Créer un commentaire

```
POST /api/projects/{project_id}/issues/{issue_id}/comments/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "description": "J'ai trouvé la source du problème dans le fichier auth.py"
}
```

### Voir le détail d'un commentaire

```
GET /api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/
Authorization: Bearer {access_token}
```

### Modifier un commentaire (auteur uniquement)

```
PATCH /api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "description": "Correction : le problème est dans le fichier models.py"
}
```

### Supprimer un commentaire (auteur uniquement)

```
DELETE /api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/
Authorization: Bearer {access_token}
```

## Scénario de Test Complet

### 1. Créer un projet (si nécessaire)

```
POST /api/projects/
{
    "name": "Mon Projet de Test",
    "description": "Un projet pour tester les issues",
    "type": "backend"
}
```

### 2. Ajouter un contributeur au projet

```
POST /api/projects/{project_id}/contributors/
{
    "user_id": 2,
    "role": "contributor"
}
```

### 3. Créer une issue

```
POST /api/projects/{project_id}/issues/
{
    "title": "Première issue",
    "description": "Description de l'issue",
    "priority": "medium",
    "status": "to_do",
    "tag": "feature"
}
```

### 4. Assigner l'issue à un contributeur

```
PATCH /api/projects/{project_id}/issues/{issue_id}/
{
    "assignee_id": 2
}
```

### 5. Ajouter un commentaire

```
POST /api/projects/{project_id}/issues/{issue_id}/comments/
{
    "description": "Je commence à travailler sur cette issue"
}
```

### 6. Modifier le statut de l'issue

```
PATCH /api/projects/{project_id}/issues/{issue_id}/
{
    "status": "in_progress"
}
```

### 7. Ajouter un autre commentaire

```
POST /api/projects/{project_id}/issues/{issue_id}/comments/
{
    "description": "Issue terminée, prête pour revue"
}
```

### 8. Finaliser l'issue

```
PATCH /api/projects/{project_id}/issues/{issue_id}/
{
    "status": "finished"
}
```

## Points de Vigilance

### Permissions

- ✅ Tous les contributeurs du projet peuvent créer des issues et commentaires
- ✅ Seul l'auteur peut modifier ou supprimer ses propres issues
- ✅ Seul l'auteur peut modifier ou supprimer ses propres commentaires
- ✅ L'assignee doit être un contributeur du projet

### Validations

- ✅ Un utilisateur doit être contributeur du projet pour créer des issues/commentaires
- ✅ Les choix de priority, status et tag sont limités aux valeurs définies
- ✅ L'assignee (si spécifié) doit être un contributeur du projet

## Test avec Postman/Insomnia

1. Importez les endpoints ci-dessus
2. Configurez l'authentification Bearer Token avec votre access_token
3. Testez chaque endpoint dans l'ordre suggéré
4. Vérifiez les codes de réponse :
   - 200 : Succès (GET, PATCH)
   - 201 : Créé (POST)
   - 204 : Supprimé (DELETE)
   - 403 : Interdit (permission refusée)
   - 404 : Non trouvé

## Test avec curl

```bash
# Obtenir la liste des issues
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/projects/1/issues/

# Créer une issue
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Issue","description":"Description","priority":"high","tag":"bug"}' \
  http://localhost:8000/api/projects/1/issues/

# Créer un commentaire
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"description":"Mon commentaire"}' \
  http://localhost:8000/api/projects/1/issues/1/comments/
```
