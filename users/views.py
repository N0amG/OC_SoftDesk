from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import UserSerializer


class RegisterView(generics.CreateAPIView):
    """Inscription d'un nouvel utilisateur - POST /api/auth/register/"""

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileView(generics.RetrieveAPIView):
    """Récupérer son propre profil - GET /api/auth/profile/"""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retourne toujours l'utilisateur authentifié."""
        return self.request.user


class UserDeleteView(generics.DestroyAPIView):
    """Supprimer son propre compte - DELETE /api/auth/profile/"""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retourne toujours l'utilisateur authentifié."""
        return self.request.user
