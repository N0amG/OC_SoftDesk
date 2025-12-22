from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import UserSerializer


class RegisterView(generics.CreateAPIView):
    """API endpoint for user registration."""

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
