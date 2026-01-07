from django.contrib import admin
from .models import Project, Contributor


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Configuration de l'interface admin pour Project."""

    list_display = ["id", "name", "type", "author", "created_time"]
    list_filter = ["type", "created_time"]
    search_fields = ["name", "description", "author__username"]
    readonly_fields = ["created_time"]

    fieldsets = [
        ("Informations du projet", {"fields": ["name", "description", "type"]}),
        ("Auteur", {"fields": ["author"]}),
        ("Dates", {"fields": ["created_time"], "classes": ["collapse"]}),
    ]


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    """Configuration de l'interface admin pour Contributor."""

    list_display = ["id", "user", "project", "role", "created_time"]
    list_filter = ["role", "created_time"]
    search_fields = ["user__username", "project__name"]
    readonly_fields = ["created_time"]

    fieldsets = [
        ("Contribution", {"fields": ["user", "project", "role"]}),
        ("Date", {"fields": ["created_time"], "classes": ["collapse"]}),
    ]
