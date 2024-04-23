from rest_framework import permissions
from configs.models import Role


class SubjectTeacherPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_staff:
            return True
        if user.role.user_type == Role.TEACHER:
            return True
        
        return False
