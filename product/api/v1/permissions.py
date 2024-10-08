from rest_framework.permissions import BasePermission, SAFE_METHODS

from users.models import Subscription


def make_payment(request):
    pass


class IsStudentOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return Subscription.objects.filter(
            user=request.user, course=obj.course, access_granted=True
        ).exists()


class ReadOnlyOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
