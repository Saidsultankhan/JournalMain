from rest_framework import permissions
from configs.models import User

class PupilDetailPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_staff:
            return True
        if obj.grade.subject_teacher_class.filter(teacher=user).exists():
            return True
        if obj.id == user.id:
            return True
        elif obj.grade.teacher.id == user.id:
            return True
        if obj.parent == user.id:
            return True
        
        return False


class PupilListPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_staff:
            return True
        
        return False