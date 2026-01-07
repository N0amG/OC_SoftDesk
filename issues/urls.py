from django.urls import path, include
from rest_framework_nested import routers
from .views import IssueViewSet, CommentViewSet

# Router principal (vide car les issues sont imbriquées dans les projets)
router = routers.DefaultRouter()

# Router imbriqué pour les issues d'un projet
# Les issues sont accessibles via /api/projects/{project_pk}/issues/
issues_router = routers.NestedDefaultRouter(
    None, r"projects", lookup="project"
)
issues_router.register(r"issues", IssueViewSet, basename="project-issues")

# Router imbriqué pour les commentaires d'une issue
# Les commentaires sont accessibles via /api/projects/{project_pk}/issues/{issue_pk}/comments/
comments_router = routers.NestedDefaultRouter(issues_router, r"issues", lookup="issue")
comments_router.register(r"comments", CommentViewSet, basename="issue-comments")

urlpatterns = [
    path("", include(issues_router.urls)),
    path("", include(comments_router.urls)),
]
