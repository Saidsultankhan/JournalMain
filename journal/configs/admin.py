from django.contrib import admin
from configs.models import (
    Subject,
    SubjectTeacher,
    DairyOfClass,
    Grade,
    Message,
    Conversation,
    Homework
)
from configs.models import Role, User


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_type']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_uz']


@admin.register(SubjectTeacher)
class SubjectTeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'teacher', 'grade', 'subject', 'name']

    def name(self, obj):
        return str(obj)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['grade', 'teacher', 'id']

    def grade(self, obj):
        return str(obj)


@admin.register(DairyOfClass)
class DairyAdmin(admin.ModelAdmin):
    list_display = ['id', 'mark']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'conversation', 'sender', 'is_changed', 'status', 'viewed_at', 'reply_id']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat_type', 'participants']

    def participants(self, obj):        
        return [str(child) for child in obj.participant.all()]
    
    participants.short_description = 'Participant'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'parents', 'childrens', 'grade', 'role', 'is_staff', 'last_login']

    def parents(self, obj):        
        return ", ".join([str(parent) for parent in obj.parent.all()])
    
    parents.short_description = 'Parent'
    
    def childrens(self, obj):
        return [str(child) for child in obj.children.all()]

    childrens.short_description = 'Children'


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'student', 'created_at', 'deadline', 'task_file', 'student_answer')