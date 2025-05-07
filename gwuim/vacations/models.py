from django.db import models
import uuid

class Vacation(models.Model):
    date = models.DateField(unique=True)
    title = models.CharField(max_length=100, default="Vacation Day")
    # Common fields
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.date} - {self.title}"
