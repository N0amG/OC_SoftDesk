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
        return obj.is_author(request.user)


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
        return obj.is_contributor(request.user)


class IsProjectAuthorForContributorManagement(permissions.BasePermission):
    """
    Permission pour l'action custom /projects/{id}/contributors/ sur ProjectViewSet.
    Seul l'auteur du projet peut ajouter des contributeurs (POST).
    Tous les contributeurs peuvent voir la liste (GET).
    """

    def has_object_permission(self, request, view, obj):
        """
        obj est toujours un Project dans ce contexte.
        """
        # GET : Tous les contributeurs peuvent voir
        if request.method in permissions.SAFE_METHODS:
            return obj.is_contributor(request.user)

        # POST : Seul l'auteur peut ajouter
        return obj.is_author(request.user)


class IsProjectAuthorForContributors(permissions.BasePermission):
    """
    Permission pour le ContributorViewSet (routes nested).
    Gère l'ajout/suppression de contributeurs individuels.
    """

    def has_permission(self, request, view):
        """
        Vérifie au niveau de la vue avant de récupérer l'objet.
        """
        # Pour POST : vérifier que l'utilisateur est l'auteur du projet
        if request.method == "POST":
            project_pk = view.kwargs.get("project_pk")
            if project_pk:
                from django.shortcuts import get_object_or_404
                from .models import Project

                project = get_object_or_404(Project, pk=project_pk)
                return project.is_author(request.user)

        # Pour GET/DELETE, on laisse passer et on vérifie dans has_object_permission
        return True

    def has_object_permission(self, request, view, obj):
        """
        obj est toujours un Contributor dans ce contexte.
        """
        # GET : Tous les contributeurs du projet peuvent voir
        if request.method in permissions.SAFE_METHODS:
            return Contributor.objects.filter(
                project=obj.project, user=request.user
            ).exists()

        # DELETE : Seul l'auteur du projet peut supprimer
        return obj.project.is_author(request.user)
