from django.shortcuts import redirect


def home(request):
    """
    Vue par défaut qui redirige les utilisateurs non connectés vers login.
    """
    if not request.user.is_authenticated:
        return redirect('/api/token/')
    return redirect('/api/auth/profile/')
