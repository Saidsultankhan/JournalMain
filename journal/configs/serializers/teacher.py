from rest_framework import serializers
from configs.models import (
    SubjectTeacher,
    User
)
from .dairy_of_class import GradeInnerSerializer
from .grade import GradeDetailSerializer


class TeacherDefaultSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'name_uz', 'name_ru', 'name_en')


class TeacherListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'name_uz', 'name_ru', 'name_en')


class TeacherDetailSerializer(serializers.ModelSerializer):
    mentor_of = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()
    grade = GradeInnerSerializer()

    class Meta:
        model = User
        fields = ('mentor_of', 'id', 'username', 'grade', 'subjects')

    def get_subjects(self, obj):
        serializer = GradeInnerSerializer(SubjectTeacher.objects.filter(teacher=obj).all(), many=True)

        return serializer.data

    def get_mentor_of(self, obj):
        serializer = GradeInnerSerializer(obj.grade)

        return serializer.data


class TeacherCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'name_uz', 'name_ru', 'name_en')
