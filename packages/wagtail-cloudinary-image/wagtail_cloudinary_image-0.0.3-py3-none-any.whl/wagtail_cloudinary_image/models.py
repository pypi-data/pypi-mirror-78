from django.db import models
from .abstract import AbstractCloudinaryImage, AbstractCloudinaryRendition


class CloudinaryImage(AbstractCloudinaryImage):
    pass


class CloudinaryRendition(AbstractCloudinaryRendition):
    image = models.ForeignKey(
        CloudinaryImage, on_delete=models.CASCADE, related_name="renditions"
    )
