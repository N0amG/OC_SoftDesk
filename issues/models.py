from django.db import models


class Issue(models.Model):
    """Représente un problème/ticket dans un projet."""

    PRIORITY_CHOICES = [
        ("low", "Faible"),
        ("medium", "Moyenne"),
        ("high", "Élevée"),
    ]

    STATUS_CHOICES = [
        ("to_do", "À faire"),
        ("in_progress", "En cours"),
        ("finished", "Terminé"),
    ]

    TAG_CHOICES = [
        ("bug", "Bug"),
        ("feature", "Fonctionnalité"),
        ("task", "Tâche"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="medium")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="to_do")
    tag = models.CharField(max_length=20, choices=TAG_CHOICES, default="task")
    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, related_name="issues"
    )
    author = models.ForeignKey(
        "users.CustomUser", on_delete=models.CASCADE, related_name="authored_issues"
    )
    assignee = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_issues",
    )
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_time"]

    def __str__(self):
        return f"{self.title} ({self.project.name})"


class Comment(models.Model):
    """Représente un commentaire sur un problème/ticket."""

    description = models.TextField()
    issue = models.ForeignKey(
        "Issue", on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        "users.CustomUser", on_delete=models.CASCADE, related_name="authored_comments"
    )
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_time"]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.issue.title}"
