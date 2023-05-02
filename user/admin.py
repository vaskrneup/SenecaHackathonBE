from django.contrib import admin

from user import models


@admin.register(models.User)
class UserModel(admin.ModelAdmin):
    pass
