from django.db import models
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=512,
    )
    sub_title = models.CharField(
        verbose_name=_("Sub Title"),
        max_length=1024,
    )

    image = models.ImageField(
        verbose_name=_("Image"),
        upload_to="/notification/image/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title
