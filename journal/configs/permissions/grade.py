from rest_framework import permissions
from configs.models import Role

class GradeDetailPermisson(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user

        if not request.user.is_authenticated:
            return False
        elif user.is_staff:
            return True
        elif obj.teacher.id == user.id:
            return True
        
        conditions = {
            Role.STUDENT: (obj.user_grade, {"pk": user.id}),
            Role.TEACHER: (obj.subject_teacher_class, {"teacher": user})
        }
        
        req, filter_args = conditions.get(str(user.role))
        obj.subject_teacher_class.filter(teacher=user)
        print(req, 'req', filter_args, 'filter_args')
        if req.filter(**filter_args).exists():
            return True


        return False


class GradeListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not request.user.is_authenticated:
            return False
        if user.is_authenticated and user.is_staff:
            return True
        if request.user.role.user_type == Role.TEACHER:
            return True
        
        return False
    