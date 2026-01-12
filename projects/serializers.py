from rest_framework import serializers
from .models import Project, Contributor
from users.models import CustomUser


class ContributorSerializer(serializers.ModelSerializer):
    """Serializer pour les contributeurs d'un projet."""

    username = serializers.CharField(source="user.username", read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source="user", write_only=True
    )

    class Meta:
        model = Contributor
        fields = ["id", "user_id", "username", "role", "created_time"]
        read_only_fields = ["id", "created_time"]

    def validate(self, data):
        """Valide qu'un contributeur n'est pas ajouté deux fois au même projet."""
        project_id = self.context.get("view").kwargs.get("project_pk")

        if project_id and data.get("user"):
            if Contributor.objects.filter(
                project_id=project_id, user=data["user"]
            ).exists():
                raise serializers.ValidationError(
                    "Cet utilisateur est déjà contributeur de ce projet."
                )

        return data


class ProjectListSerializer(serializers.ModelSerializer):
    """Serializer pour la liste des projets (vue allégée)."""

    author_username = serializers.CharField(source="author.username", read_only=True)
    contributors_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "type",
            "author_username",
            "contributors_count",
            "created_time",
        ]
        read_only_fields = ["id", "created_time"]

    def get_contributors_count(self, obj):
        """Retourne le nombre de contributeurs du projet."""
        return obj.contributors.count()


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Serializer pour le détail d'un projet - imbrication limitée (1 niveau)."""

    author_username = serializers.CharField(source="author.username", read_only=True)
    # Liste uniquement les IDs et usernames pour alléger la réponse
    contributors_list = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "type",
            "author_username",
            "contributors_list",
            "created_time",
        ]
        read_only_fields = ["id", "created_time"]

    def get_contributors_list(self, obj):
        """Retourne une liste simplifiée des contributeurs (1 niveau d'imbrication)."""
        return [
            {
                "id": contributor.id,
                "user_id": contributor.user.id,
                "username": contributor.user.username,
                "role": contributor.role,
            }
            for contributor in obj.contributors.all()
        ]

    def create(self, validated_data):
        """
        Crée un projet et ajoute automatiquement l'auteur comme contributeur.
        """
        # L'auteur est déjà dans validated_data (passé par perform_create)
        project = Project.objects.create(**validated_data)

        # Ajoute automatiquement l'auteur comme contributeur avec le rôle "author"
        Contributor.objects.create(
            project=project, user=validated_data["author"], role=Contributor.ROLE_AUTHOR
        )

        return project
