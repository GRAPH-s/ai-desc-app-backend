from django.db import models
from django.contrib.auth import get_user_model
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill


class RequestHistory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    user_description = models.TextField(blank=True, null=True)
    ai_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = ProcessedImageField(upload_to="images", format="WEBP")
    image_thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFill(200, 200)],
        format="WEBP",
        options={"quality": 80},
    )
