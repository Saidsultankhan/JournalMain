from rest_framework import serializers
from configs.models import (
    DairyOfClass,
    Grade,
    Subject,
    User,
    SubjectTeacher,
    Role
)
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import AuthenticationFailed


class TeacherInnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')

class GradeInnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = ('id', '__str__')


class PupilInnserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class SubjectInnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ('id', 'name_uz')


class ParentInnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'role')


class DairyDetailSerializer(serializers.ModelSerializer):
    subject_name = serializers.SerializerMethodField()
    teacher = serializers.SerializerMethodField()
    pupil = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()

    class Meta:
        model = DairyOfClass
        fields = ('mark', 'subject_name', 'quarter', 'teacher', 'pupil', 'grade')

    def get_subject_name(self, obj):
        serializer = SubjectInnerSerializer(obj.subject)

        return serializer.data

    def get_teacher(self, obj):
        serializer = TeacherInnerSerializer(obj.subject.subject_teacher_subject.first().teacher)

        return serializer.data

    def get_pupil(self, obj):
        serializer = PupilInnserSerializer(obj.pupil)

        return serializer.data

    def get_grade(self, obj):
        serializer = GradeInnerSerializer(obj.grade)
        
        return serializer.data


class DairyListSerializer(serializers.ModelSerializer):
    subject_name = serializers.SerializerMethodField()
    teacher = serializers.SerializerMethodField()
    pupil = serializers.SerializerMethodField()

    class Meta:
        model = DairyOfClass
        fields = ('id', 'mark', 'subject_name', 'quarter', 'teacher', 'pupil')

    def get_subject_name(self, obj):
        serializer = SubjectInnerSerializer(obj.subject)

        return serializer.data

    def get_teacher(self, obj):
        serializer = TeacherInnerSerializer(obj.subject.subject_teacher_subject.first().teacher)

        return serializer.data

    def get_pupil(self, obj):
        serializer = PupilInnserSerializer(obj.pupil)

        return serializer.data


class DairyUpdateSerializer(serializers.ModelSerializer):
    mark = serializers.IntegerField(required=False)
    pupil = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role__user_type=Role.STUDENT), required=False)
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), required=False)
    quarter = serializers.IntegerField(required=False)
    grade = serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all(), required=False)

    class Meta:
        model = DairyOfClass
        fields = '__all__'


class DairyDefaultSerializer(serializers.ModelSerializer):

    class Meta:
        model = DairyOfClass
        fields = '__all__'


class DairyCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = DairyOfClass
        fields = ('mark', 'quarter', 'pupil', 'subject', 'grade')

    def create(self, validated_data):
        message = {
            'detail': "У вас нет прав для добавления оценок в этот класс или по данному предмету."
        }
        request_user = self.context["request"].user
        
        if request_user.role and request_user.role.user_type == Role.TEACHER:
            teacher = request_user
        else:
            teacher = False

        if teacher:
            subject = validated_data.get('subject')
            coming_grade = validated_data.get('grade')
            pupils_grade = validated_data['pupil'].grade

            if SubjectTeacher.objects.filter(
                teacher=teacher, 
                subject=subject, 
                grade=pupils_grade, 
                grade_id=coming_grade.id
                ).exists():
                return DairyOfClass.objects.create(**validated_data)
            
        raise PermissionDenied(message)
    
