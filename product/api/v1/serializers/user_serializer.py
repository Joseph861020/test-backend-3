from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Subscription
from courses.models import Course

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'date_joined',
        )

class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор курсов для подписки."""

    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            # Добавьте другие поля, если нужно
        )

class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""

    user = CustomUserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    subscription_date = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')  # Можно настроить формат даты и времени
    access_granted = serializers.BooleanField()

    class Meta:
        model = Subscription
        fields = (
            'id',
            'user',
            'course',
            'access_granted',
            'subscription_date',
        )
