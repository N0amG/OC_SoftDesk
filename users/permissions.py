"""
Classes de permissions personnalisées pour l'application users.

Les permissions des users sont simples :
- RegisterView : AllowAny (n'importe qui peut s'inscrire)
- UserProfileView : IsAuthenticated (seul l'utilisateur authentifié peut voir son profil)
- UserDeleteView : IsAuthenticated (seul l'utilisateur authentifié peut supprimer son compte)

Ces permissions sont déjà appliquées dans views.py et respectent le RGPD :
- L'utilisateur ne peut voir que son propre profil (confidentialité)
- L'utilisateur peut supprimer son compte (droit à l'oubli)
- La suppression est réelle (CASCADE), pas de "soft delete"
"""
from rest_framework import permissions


class IsSelfUser(permissions.BasePermission):
    """
    Permission qui autorise un utilisateur à accéder uniquement à son propre profil.
    Cette permission est redondante avec get_object() qui retourne request.user,
    mais elle est documentée ici pour la clarté.
    """

    def has_object_permission(self, request, view, obj):
        """
        Vérifie que l'objet User correspond à l'utilisateur authentifié.
        """
        return obj == request.user
