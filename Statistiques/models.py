from django.db import models

# Create your models here.
# models.py
from django.db import models
from django.conf import settings

class Content(models.Model):
    title = models.CharField(max_length=255)
    content_type = models.CharField(max_length=50)  # e.g., Movie, Series, Live Event

    def __str__(self):
        return self.title

class ViewingStatistics(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    view_date = models.DateTimeField(auto_now_add=True)
    duration_seconds = models.PositiveIntegerField()  # Duration of the view in seconds

    def __str__(self):
        return f"{self.user.username} - {self.content.title} on {self.view_date}"

class ContentPerformance(models.Model):
    content = models.OneToOneField(Content, on_delete=models.CASCADE)
    views_count = models.PositiveIntegerField(default=0)
    average_duration = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # in seconds

    def __str__(self):
        return f"{self.content.title} - Views: {self.views_count}, Avg Duration: {self.average_duration}"

class UserEngagement(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_views = models.PositiveIntegerField(default=0)
    total_duration = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # in seconds

    def __str__(self):
        return f"{self.user.username} - Total Views: {self.total_views}, Total Duration: {self.total_duration}"
