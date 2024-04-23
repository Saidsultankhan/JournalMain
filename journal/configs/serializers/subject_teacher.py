from rest_framework import serializers
from configs.models import SubjectTeacher
from .dairy_of_class import (
    SubjectInnerSerializer,
    GradeInnerSerializer,
    TeacherInnerSerializer,
)


class SubjectTeacherDetailSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    grades = serializers.SerializerMethodField()

    class Meta:
        model = SubjectTeacher
        fields = ('id', 'teacher', 'subject', 'grades')

    def get_teacher(self, obj):
        serializer = TeacherInnerSerializer(obj.teacher)

        return serializer.data

    def get_subject(self, obj):
        serializer = SubjectInnerSerializer(obj.subject)

        return serializer.data

    def get_grades(self, obj):
        serializer = GradeInnerSerializer(obj.grade)

        return serializer.data


class SubjectTeacherListSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()
    teacher = serializers.SerializerMethodField()

    class Meta:
        model = SubjectTeacher
        fields = ('id', 'subject', 'teacher')

    def get_subject(self, obj):
        serializer = SubjectInnerSerializer(obj.subject)
        
        return serializer.data

    def get_teacher(self, obj):
        serializer = TeacherInnerSerializer(obj.subject.subject_teacher_subject.first().teacher)

        return serializer.data
    

class SubjectTeacherDefaultSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubjectTeacher
        fields = ('teacher', 'subject', 'grade')
