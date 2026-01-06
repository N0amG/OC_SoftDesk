from django.urls import path, include
from rest_framework_nested import routers
from .views import ProjectViewSet, ContributorViewSet

# Router principal pour les projets
router = routers.DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")

# Router imbriqué pour les contributeurs d'un projet
projects_router = routers.NestedDefaultRouter(router, r"projects", lookup="project")
projects_router.register(
    r"contributors", ContributorViewSet, basename="project-contributors"
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(projects_router.urls)),
]
