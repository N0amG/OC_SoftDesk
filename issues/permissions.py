"""
Classes de permissions personnalisées pour l'application issues.
"""

from rest_framework import permissions
from projects.models import Contributor


class IsIssueAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission qui autorise :
    - Lecture (GET) pour tous les contributeurs du projet
    - Modification/Suppression (PUT, PATCH, DELETE) uniquement pour l'auteur de l'issue
    """

    # S'execute avant reception de la view
    def has_permission(self, request, view):
        """
        Vérifie au niveau de la vue si l'utilisateur peut accéder aux issues.
        """
        # Vérifie que l'utilisateur est contributeur du projet
        project_pk = view.kwargs.get("project_pk")
        if project_pk:
            return Contributor.objects.filter(
                project_id=project_pk, user=request.user
            ).exists()
        return False

    # S'execute apres reception de l'objet
    def has_object_permission(self, request, view, obj):
        """
        Vérifie si l'utilisateur peut effectuer l'action sur l'issue.
        obj est une instance d'Issue.
        """
        # Les méthodes de lecture (GET, HEAD, OPTIONS) sont autorisées pour tous les contributeurs
        if request.method in permissions.SAFE_METHODS:
            # Vérifie que l'utilisateur est contributeur du projet de l'issue
            return Contributor.objects.filter(
                project=obj.project, user=request.user
            ).exists()

        # Les méthodes d'écriture (PUT, PATCH, DELETE) sont autorisées uniquement pour l'auteur
        return obj.author == request.user


class IsCommentAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission qui autorise :
    - Lecture (GET) pour tous les contributeurs du projet
    - Modification/Suppression (PUT, PATCH, DELETE) uniquement pour l'auteur du commentaire
    """

    def has_permission(self, request, view):
        """
        Vérifie au niveau de la vue si l'utilisateur peut accéder aux commentaires.
        """
        # Récupère le projet via l'issue
        issue_pk = view.kwargs.get("issue_pk")
        if issue_pk:
            from .models import Issue

            try:
                issue = Issue.objects.get(pk=issue_pk)
                # Vérifie que l'utilisateur est contributeur du projet
                return Contributor.objects.filter(
                    project=issue.project, user=request.user
                ).exists()
            except Issue.DoesNotExist:
                return False
        return False

    def has_object_permission(self, request, view, obj):
        """
        Vérifie si l'utilisateur peut effectuer l'action sur le commentaire.
        obj est une instance de Comment.
        """
        # Les méthodes de lecture (GET, HEAD, OPTIONS) sont autorisées pour tous les contributeurs
        if request.method in permissions.SAFE_METHODS:
            # Vérifie que l'utilisateur est contributeur du projet du commentaire
            return Contributor.objects.filter(
                project=obj.issue.project, user=request.user
            ).exists()

        # Les méthodes d'écriture (PUT, PATCH, DELETE) sont autorisées uniquement pour l'auteur
        return obj.author == request.user
