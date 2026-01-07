from django.urls import path, include
from rest_framework_nested import routers
from .views import ProjectViewSet, ContributorViewSet
from issues.views import IssueViewSet, CommentViewSet

# Router principal pour les projets
router = routers.DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")

# Router imbriqué pour les contributeurs d'un projet
projects_router = routers.NestedDefaultRouter(router, r"projects", lookup="project")
projects_router.register(
    r"contributors", ContributorViewSet, basename="project-contributors"
)

# Router imbriqué pour les issues d'un projet
projects_router.register(r"issues", IssueViewSet, basename="project-issues")

# Router imbriqué pour les commentaires d'une issue
issues_router = routers.NestedDefaultRouter(projects_router, r"issues", lookup="issue")
issues_router.register(r"comments", CommentViewSet, basename="issue-comments")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(projects_router.urls)),
    path("", include(issues_router.urls)),
]
