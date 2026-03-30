from rest_framework import serializers
from userManagement.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = "__all__"

class loginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
