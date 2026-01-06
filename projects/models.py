from django.db import models


class Project(models.Model):
    """Représente un projet de développement."""

    # 1er élément = stocké en bdd, 2ème élément = affiché dans le champ de sélection
    TYPE_CHOICES = [
        ("backend", "Back-end"),
        ("frontend", "Front-end"),
        ("ios", "iOS"),
        ("android", "Android"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    author = models.ForeignKey(
        "users.CustomUser", on_delete=models.CASCADE, related_name="authored_projects"
    )
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_time"]

    def __str__(self):
        return f"{self.name} ({self.type})"


class Contributor(models.Model):
    """
    Table intermédiaire entre User et Project.
    Représente un contributeur sur un projet avec son rôle.
    """

    ROLE_CHOICES = [
        ("author", "Autheur"),
        ("contributor", "Contributeur"),
    ]

    user = models.ForeignKey(
        "users.CustomUser", on_delete=models.CASCADE, related_name="contributions"
    )
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="contributors"
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "project"]
        ordering = ["-created_time"]

    def __str__(self):
        return f"{self.user.username} - {self.project.name} ({self.role})"
