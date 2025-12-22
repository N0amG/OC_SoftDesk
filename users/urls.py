from django.urls import path
from .views import RegisterView, UserProfileView, UserDeleteView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/delete/', UserDeleteView.as_view(), name='profile-delete'),
]
