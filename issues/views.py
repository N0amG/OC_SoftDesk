from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Issue, Comment
from .serializers import IssueListSerializer, IssueDetailSerializer, CommentSerializer
from .permissions import IsIssueAuthorOrReadOnly, IsCommentAuthorOrReadOnly
from projects.models import Project


class IssueViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les problèmes/tickets d'un projet.

    - list: Liste tous les problèmes du projet (contributeurs)
    - retrieve: Détail d'un problème (contributeurs)
    - create: Crée un nouveau problème (contributeurs)
    - update/partial_update: Modifie un problème (auteur uniquement)
    - destroy: Supprime un problème (auteur uniquement)

    Permissions :
    - IsAuthenticated : utilisateur authentifié requis
    - IsIssueAuthorOrReadOnly : contributeur peut lire, auteur peut modifier/supprimer
    """

    permission_classes = [IsAuthenticated, IsIssueAuthorOrReadOnly]

    def get_queryset(self):
        """Retourne les problèmes du projet spécifié.
        Optimisé avec select_related et prefetch_related.
        """
        project_pk = self.kwargs.get("project_pk")
        return (
            Issue.objects.filter(project_id=project_pk)
            .select_related("author", "assignee", "project")  # Charge en une requête
            .prefetch_related("comments")  # Charge les commentaires si nécessaire
        )

    def get_serializer_class(self):
        """Utilise un serializer différent selon l'action."""
        if self.action in ["retrieve", "create", "update", "partial_update"]:
            return IssueDetailSerializer
        return IssueListSerializer

    def perform_create(self, serializer):
        """
        L'auteur est automatiquement l'utilisateur connecté.
        Le projet est automatiquement celui de l'URL.
        Les permissions sont vérifiées par IsIssueAuthorOrReadOnly.
        """
        project_pk = self.kwargs.get("project_pk")
        project = get_object_or_404(Project, pk=project_pk)

        serializer.save(author=self.request.user, project=project)

    # Les permissions update et destroy sont gérées automatiquement par IsIssueAuthorOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les commentaires d'un problème.

    - list: Liste tous les commentaires du problème (contributeurs)
    - retrieve: Détail d'un commentaire (contributeurs)
    - create: Crée un nouveau commentaire (contributeurs)
    - update/partial_update: Modifie un commentaire (auteur uniquement)
    - destroy: Supprime un commentaire (auteur uniquement)

    Permissions :
    - IsAuthenticated : utilisateur authentifié requis
    - IsCommentAuthorOrReadOnly : contributeur peut lire, auteur peut modifier/supprimer
    """

    permission_classes = [IsAuthenticated, IsCommentAuthorOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Retourne les commentaires du problème spécifié.
        Optimisé avec select_related.
        """
        issue_pk = self.kwargs.get("issue_pk")
        return (
            Comment.objects.filter(issue_id=issue_pk)
            .select_related("author", "issue")  # Charge en une requête
        )

    def perform_create(self, serializer):
        """
        L'auteur est automatiquement l'utilisateur connecté.
        Le problème est automatiquement celui de l'URL.
        Les permissions sont vérifiées par IsCommentAuthorOrReadOnly.
        """
        issue_pk = self.kwargs.get("issue_pk")
        issue = Issue.objects.get(pk=issue_pk)

        serializer.save(author=self.request.user, issue=issue)

    # Les permissions update et destroy sont gérées automatiquement par IsCommentAuthorOrReadOnly
