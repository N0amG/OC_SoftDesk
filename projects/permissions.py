"""
Classes de permissions personnalisées pour l'application projects.
"""
from rest_framework import permissions
from .models import Contributor


class IsProjectAuthor(permissions.BasePermission):
    """
    Permission qui n'autorise que l'auteur d'un projet à le modifier/supprimer.
    """

    def has_object_permission(self, request, view, obj):
        """
        Vérifie si l'utilisateur est l'auteur du projet.
        obj est une instance de Project.
        """
        # Les méthodes de lecture (GET, HEAD, OPTIONS) sont autorisées pour tous les contributeurs
        if request.method in permissions.SAFE_METHODS:
            return True

        # Les méthodes d'écriture (PUT, PATCH, DELETE) sont autorisées uniquement pour l'auteur
        return obj.author == request.user


class IsProjectContributor(permissions.BasePermission):
    """
    Permission qui vérifie que l'utilisateur est contributeur du projet.
    Utilisée pour GET uniquement (lecture seule).
    """

    def has_permission(self, request, view):
        """
        Vérifie au niveau de la vue si l'utilisateur peut accéder aux projets.
        Pour list et create, on laisse passer et on filtre dans get_queryset.
        """
        return True

    def has_object_permission(self, request, view, obj):
        """
        Vérifie si l'utilisateur est contributeur du projet.
        obj est une instance de Project.
        """
        # Vérifie que l'utilisateur est contributeur du projet
        return Contributor.objects.filter(project=obj, user=request.user).exists()


class IsProjectAuthorForContributors(permissions.BasePermission):
    """
    Permission pour gérer les contributeurs : seul l'auteur du projet peut ajouter/supprimer des contributeurs.
    """

    def has_permission(self, request, view):
        """
        Vérifie au niveau de la vue.
        Pour GET (list), on autorise tous les contributeurs.
        Pour POST/DELETE, on vérifie dans has_object_permission.
        """
        # Pour la création (POST), on doit vérifier le projet
        if request.method == "POST":
            # Le project_pk vient de l'URL
            project_pk = view.kwargs.get("project_pk")
            if project_pk:
                from .models import Project

                try:
                    project = Project.objects.get(pk=project_pk)
                    # Seul l'auteur peut ajouter des contributeurs
                    return project.author == request.user
                except Project.DoesNotExist:
                    return False
        return True

    def has_object_permission(self, request, view, obj):
        """
        Vérifie au niveau de l'objet (Contributor).
        obj est une instance de Contributor.
        """
        # Les méthodes de lecture sont autorisées pour tous les contributeurs du projet
        if request.method in permissions.SAFE_METHODS:
            # Vérifie que l'utilisateur est contributeur du projet
            return Contributor.objects.filter(
                project=obj.project, user=request.user
            ).exists()

        # Les méthodes d'écriture (PUT, PATCH, DELETE) sont autorisées uniquement pour l'auteur
        return obj.project.author == request.user
