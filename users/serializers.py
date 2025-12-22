from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user registration and details."""

    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "password",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        """Create a new user with encrypted password."""
        # On enlève le mot de passe des données lisibles pour le passer à create_user qui le hashera
        password = validated_data.pop("password")
        return CustomUser.objects.create_user(password=password, **validated_data)
