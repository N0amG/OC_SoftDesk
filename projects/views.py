from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Project, Contributor
from .serializers import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    ContributorSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les projets.

    - list: Liste tous les projets où l'utilisateur est contributeur
    - retrieve: Détail d'un projet
    - create: Crée un nouveau projet
    - update/partial_update: Modifie un projet
    - destroy: Supprime un projet
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retourne uniquement les projets où l'utilisateur est contributeur.
        Est automatiquement appelé par les actions list, retrieve, update, destroy.
        """
        user = self.request.user
        # Récupère tous les projets où l'utilisateur est contributeur
        return Project.objects.filter(contributors__user=user).distinct()

    def get_serializer_class(self):
        """Utilise un serializer différent selon l'action."""
        if self.action in ["retrieve", "create"]:
            return ProjectDetailSerializer
        return ProjectListSerializer

    def perform_create(self, serializer):
        """
        L'auteur est automatiquement l'utilisateur connecté.
        perform_create est appelé avant create().
        """
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["get", "post"])
    def contributors(self, request, pk=None):
        """
        GET: Liste les contributeurs d'un projet
        POST: Ajoute un contributeur à un projet
        """
        project = self.get_object()

        if request.method == "GET":
            contributors = project.contributors.all()
            serializer = ContributorSerializer(contributors, many=True)
            return Response(serializer.data)

        elif request.method == "POST":
            # Seul l'auteur peut ajouter des contributeurs
            if project.author != request.user:
                return Response(
                    {
                        "detail": "Seul l'auteur du projet peut ajouter des contributeurs."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            serializer = ContributorSerializer(
                data=request.data, context={"request": request, "view": self}
            )

            if serializer.is_valid():
                serializer.save(project=project)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContributorViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les contributeurs.
    Accessible via /api/projects/{project_pk}/contributors/
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ContributorSerializer

    def get_queryset(self):
        """Retourne les contributeurs du projet spécifié."""
        project_pk = self.kwargs.get("project_pk")
        return Contributor.objects.filter(project_id=project_pk)

    def perform_create(self, serializer):
        """Ajoute un contributeur au projet."""
        project_pk = self.kwargs.get("project_pk")
        project = Project.objects.get(pk=project_pk)

        # Vérifie que seul l'auteur peut ajouter des contributeurs
        if project.author != self.request.user:
            return Response(
                {"detail": "Seul l'auteur du projet peut ajouter des contributeurs."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Par défaut, le rôle est "contributor"
        serializer.save(project=project, role="contributor")

    def destroy(self, request, *args, **kwargs):
        """Supprime un contributeur d'un projet."""
        contributor = self.get_object()
        project = contributor.project

        # Vérifie que seul l'auteur peut supprimer des contributeurs
        if project.author != request.user:
            return Response(
                {"detail": "Seul l'auteur du projet peut supprimer des contributeurs."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Empêche la suppression de l'auteur lui-même
        if contributor.role == "author":
            return Response(
                {"detail": "L'auteur du projet ne peut pas être retiré."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().destroy(request, *args, **kwargs)
