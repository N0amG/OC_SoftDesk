from rest_framework import serializers
from .models import Issue, Comment
from users.models import CustomUser


class CommentSerializer(serializers.ModelSerializer):
    """Serializer pour les commentaires d'un problème."""

    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "description", "author_username", "issue", "created_time"]
        read_only_fields = ["id", "created_time", "issue"]


class IssueListSerializer(serializers.ModelSerializer):
    """Serializer pour la liste des problèmes (vue allégée)."""

    author_username = serializers.CharField(source="author.username", read_only=True)
    assignee_username = serializers.CharField(
        source="assignee.username", read_only=True, allow_null=True
    )
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "priority",
            "status",
            "tag",
            "author_username",
            "assignee_username",
            "comments_count",
            "created_time",
        ]
        read_only_fields = ["id", "created_time"]

    def get_comments_count(self, obj):
        """Retourne le nombre de commentaires du problème."""
        return obj.comments.count()


class IssueDetailSerializer(serializers.ModelSerializer):
    """Serializer pour le détail d'un problème avec tous les commentaires."""

    author_username = serializers.CharField(source="author.username", read_only=True)
    assignee_username = serializers.CharField(
        source="assignee.username", read_only=True, allow_null=True
    )
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source="assignee", required=False, allow_null=True
    )
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "priority",
            "status",
            "tag",
            "author_username",
            "assignee_username",
            "assignee_id",
            "comments",
            "project",
            "created_time",
        ]
        read_only_fields = ["id", "created_time", "project"]

    def validate_assignee_id(self, value):
        """Valide que l'assignee est un contributeur du projet."""
        if value:
            project_id = self.context.get("view").kwargs.get("project_pk")
            if project_id:
                from projects.models import Contributor

                if not Contributor.objects.filter(
                    project_id=project_id, user=value
                ).exists():
                    raise serializers.ValidationError(
                        "L'assignee doit être un contributeur du projet."
                    )
        return value
