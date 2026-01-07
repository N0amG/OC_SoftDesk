from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Issue, Comment
from .serializers import IssueListSerializer, IssueDetailSerializer, CommentSerializer
from projects.models import Project, Contributor


class IssueViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les problèmes/tickets d'un projet.

    - list: Liste tous les problèmes du projet
    - retrieve: Détail d'un problème
    - create: Crée un nouveau problème
    - update/partial_update: Modifie un problème
    - destroy: Supprime un problème
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retourne les problèmes du projet spécifié."""
        project_pk = self.kwargs.get("project_pk")
        return Issue.objects.filter(project_id=project_pk)

    def get_serializer_class(self):
        """Utilise un serializer différent selon l'action."""
        if self.action in ["retrieve", "create", "update", "partial_update"]:
            return IssueDetailSerializer
        return IssueListSerializer

    def perform_create(self, serializer):
        """
        L'auteur est automatiquement l'utilisateur connecté.
        Le projet est automatiquement celui de l'URL.
        """
        project_pk = self.kwargs.get("project_pk")
        project = Project.objects.get(pk=project_pk)

        # Vérifie que l'utilisateur est contributeur du projet
        if not Contributor.objects.filter(
            project=project, user=self.request.user
        ).exists():
            return Response(
                {"detail": "Vous devez être contributeur du projet."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer.save(author=self.request.user, project=project)

    def update(self, request, *args, **kwargs):
        """Seul l'auteur peut modifier un problème."""
        issue = self.get_object()
        if issue.author != request.user:
            return Response(
                {"detail": "Seul l'auteur peut modifier ce problème."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Seul l'auteur peut supprimer un problème."""
        issue = self.get_object()
        if issue.author != request.user:
            return Response(
                {"detail": "Seul l'auteur peut supprimer ce problème."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les commentaires d'un problème.

    - list: Liste tous les commentaires du problème
    - retrieve: Détail d'un commentaire
    - create: Crée un nouveau commentaire
    - update/partial_update: Modifie un commentaire
    - destroy: Supprime un commentaire
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Retourne les commentaires du problème spécifié."""
        issue_pk = self.kwargs.get("issue_pk")
        return Comment.objects.filter(issue_id=issue_pk)

    def perform_create(self, serializer):
        """
        L'auteur est automatiquement l'utilisateur connecté.
        Le problème est automatiquement celui de l'URL.
        """
        issue_pk = self.kwargs.get("issue_pk")
        issue = Issue.objects.get(pk=issue_pk)

        # Vérifie que l'utilisateur est contributeur du projet
        if not Contributor.objects.filter(
            project=issue.project, user=self.request.user
        ).exists():
            return Response(
                {"detail": "Vous devez être contributeur du projet."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer.save(author=self.request.user, issue=issue)

    def update(self, request, *args, **kwargs):
        """Seul l'auteur peut modifier un commentaire."""
        comment = self.get_object()
        if comment.author != request.user:
            return Response(
                {"detail": "Seul l'auteur peut modifier ce commentaire."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Seul l'auteur peut supprimer un commentaire."""
        comment = self.get_object()
        if comment.author != request.user:
            return Response(
                {"detail": "Seul l'auteur peut supprimer ce commentaire."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)
