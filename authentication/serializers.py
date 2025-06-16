from rest_framework import serializers

from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "role",
            "first_name",
            "last_name",
            "city",
            "password",
            "password_confirm",
        )

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("Пароли не совпадают")
        if data.get("role") == User.Role.ADMIN:
            raise serializers.ValidationError("Нельзя выбрать роль администратора")
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirm")  # убираем поле, не относящееся к модели
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user
