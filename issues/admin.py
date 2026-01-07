from django.contrib import admin
from .models import Issue, Comment


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    """Interface d'administration pour les Issues."""

    list_display = ["id", "title", "project", "status", "priority", "tag", "author", "assignee", "created_time"]
    list_filter = ["status", "priority", "tag", "created_time"]
    search_fields = ["title", "description", "project__name"]
    readonly_fields = ["created_time"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Interface d'administration pour les Comments."""

    list_display = ["id", "issue", "author", "created_time"]
    list_filter = ["created_time"]
    search_fields = ["description", "issue__title"]
    readonly_fields = ["created_time"]
