from rest_framework import serializers
from user import models as user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model.User
        fields = ["first_name", "last_name", "government_id", "email", "is_active", "is_staff"]
