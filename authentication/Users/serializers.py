from rest_framework import serializers
from Users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    """Registration serializer with password checkup"""

    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True
    )
    Confirm_Password = serializers.CharField(
        max_length=68, min_length=6, write_only=True
    )

    class Meta:
        model = User
        fields = ["email",'first_name','last_name', "password", "Confirm_Password"]

    def validate(self, data):
        if data['first_name'] is None:
            raise serializers.ValidationError(
                {"details": "first name must not be null"}
            )
        if data['last_name'] is None:
            raise serializers.ValidationError(
                {"details": "last name must not be null"}
            )
        if data["password"] != data["Confirm_Password"]:
            raise serializers.ValidationError(
                {"details": "Passwords does not match"}
            )
        return data

    def create(self, validated_data):
        validated_data.pop("Confirm_Password")
        return User.objects.create_user(**validated_data)
