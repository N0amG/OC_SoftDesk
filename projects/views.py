from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Project, Contributor
from .serializers import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    ContributorSerializer,
)
from .permissions import (
    IsProjectAuthor,
    IsProjectContributor,
    IsProjectAuthorForContributorManagement,
    IsProjectAuthorForContributors,
)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les projets.

    - list: Liste tous les projets où l'utilisateur est contributeur
    - retrieve: Détail d'un projet
    - create: Crée un nouveau projet
    - update/partial_update: Modifie un projet (auteur uniquement)
    - destroy: Supprime un projet (auteur uniquement)

    Permissions :
    - IsAuthenticated : utilisateur authentifié requis
    - IsProjectContributor : doit être contributeur pour accéder au projet
    - IsProjectAuthor : doit être auteur pour modifier/supprimer
    """

    permission_classes = [IsAuthenticated, IsProjectContributor, IsProjectAuthor]

    def get_queryset(self):
        """
        Retourne uniquement les projets où l'utilisateur est contributeur.
        Est automatiquement appelé par les actions list, retrieve, update, destroy.
        Optimisé avec select_related et prefetch_related pour éviter les requêtes N+1.
        """
        user = self.request.user
        # Optimisation : charge l'auteur et les contributeurs en une seule requête
        queryset = (
            Project.objects.filter(contributors__user=user)
            .select_related("author")  # Charge l'auteur en une requête
            .prefetch_related("contributors__user")  # Charge les contributeurs
            .distinct()
        )
        return queryset

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

    @action(
        detail=True,
        methods=["get", "post"],
        permission_classes=[IsAuthenticated, IsProjectAuthorForContributorManagement],
    )
    def contributors(self, request, pk=None):
        """
        GET: Liste les contributeurs d'un projet (tous les contributeurs)
        POST: Ajoute un contributeur à un projet (auteur uniquement)

        Les permissions sont gérées par IsProjectAuthorForContributorManagement.
        """
        project = self.get_object()

        if request.method == "GET":
            contributors = project.contributors.all()
            serializer = ContributorSerializer(contributors, many=True)
            return Response(serializer.data)

        elif request.method == "POST":
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

    Permissions :
    - IsAuthenticated : utilisateur authentifié requis
    - IsProjectAuthorForContributors : gère les permissions de lecture/écriture
    """

    permission_classes = [IsAuthenticated, IsProjectAuthorForContributors]
    serializer_class = ContributorSerializer

    def get_queryset(self):
        """Retourne les contributeurs du projet spécifié.
        Optimisé avec select_related pour charger les users.
        """
        project_pk = self.kwargs.get("project_pk")
        return (
            Contributor.objects.filter(project_id=project_pk)
            .select_related("user", "project")  # Charge user et project en une requête
        )

    def perform_create(self, serializer):
        """
        Ajoute un contributeur au projet.
        Les permissions sont vérifiées par IsProjectAuthorForContributors.
        """
        project_pk = self.kwargs.get("project_pk")
        project = get_object_or_404(Project, pk=project_pk)

        # Par défaut, le rôle est "contributor"
        serializer.save(project=project, role=Contributor.ROLE_CONTRIBUTOR)

    def destroy(self, request, *args, **kwargs):
        """
        Supprime un contributeur d'un projet.
        Les permissions sont vérifiées par IsProjectAuthorForContributors.
        """
        contributor = self.get_object()

        # Empêche la suppression de l'auteur lui-même
        if contributor.role == Contributor.ROLE_AUTHOR:
            return Response(
                {"detail": "L'auteur du projet ne peut pas être retiré."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().destroy(request, *args, **kwargs)
