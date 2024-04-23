from rest_framework import permissions
from configs.models import Role

class DairyTeacher(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        

    def has_object_permission(self, request, view, obj):
        return (
                request.user.is_authenticated and
                (request.user.is_staff or obj.subject.subject_teacher_subject.filter(
                    teacher=request.user,
                    grade=obj.grade).exists()
                )
            )


class DairyListTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff or request.user.role.user_type == Role.TEACHER:
            return True
