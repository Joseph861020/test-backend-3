from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course
from rest_framework.viewsets import ModelViewSet
from users.models import Subscription


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all()


class CourseViewSet(ModelViewSet):
    """Курсы"""

    queryset = Course.objects.all()
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""

        course = get_object_or_404(Course, id=pk)
        user = request.user

        # Check if the user already has an active subscription for this course
        existing_subscription = Subscription.objects.filter(user=user, course=course).first()
        if existing_subscription:
            return Response(
                {"detail": "Вы уже подписаны на этот курс."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the user has sufficient balance
        user_balance = user.balance.balance
        if user_balance < course.price:
            return Response(
                {"detail": "Недостаточно средств на балансе."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the subscription
        subscription = Subscription.objects.create(
            user=user,
            course=course,
            access_granted=True,
            subscription_date=timezone.now()
        )

        # Update the user's balance
        user_balance -= course.price
        user.balance.balance = user_balance
        user.balance.save()

        serializer = SubscriptionSerializer(subscription)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )