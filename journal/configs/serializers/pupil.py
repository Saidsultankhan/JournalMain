from rest_framework import serializers
from django.db.models import Avg
from configs.models import (
    User,
    DairyOfClass,
    SubjectTeacher
)
from .dairy_of_class import (
    GradeInnerSerializer,
    SubjectInnerSerializer,
    ParentInnerSerializer
)


class PupilBaseSerializer(serializers.ModelSerializer):
    average_mark = serializers.SerializerMethodField()

    def get_average_mark(self, obj):

        return obj.dairy_pupil.aggregate(average_mark=Avg('mark'))['average_mark']


class PupilDetailSerializer(PupilBaseSerializer):
    pupils_dairy = serializers.SerializerMethodField(source='dairy_pupils')
    grade = serializers.SerializerMethodField()
    teachers = serializers.SerializerMethodField()
    parents = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'name_en', 'name_ru', 'name_uz', 'grade', 'average_mark', 'pupils_dairy', 'teachers', 'parents')

    def get_pupils_dairy(self, obj):
        unique_subjects = DairyOfClass.objects.filter(
            pupil__id=obj.id
        ).values_list('subject__name_uz', flat=True).distinct()

        subjects_data = []
        for subject in unique_subjects:
            average_mark = DairyOfClass.objects.filter(
                subject__name_uz=subject,
                pupil__id=obj.id
            ).aggregate(average_mark=Avg('mark'))['average_mark']

            # subject_marks = self.get_subject_marks(obj, subject)
            subjects_data.append({
                'subject_name': subject,
                'average_subject_mark': average_mark,
                # f'all_marks_in_{subject}': subject_marks
            })

        return subjects_data

    def get_teachers(self, obj):
        serializer = SubjectInnerSerializer(
            SubjectTeacher.
            objects.filter(grade=obj.grade).
            select_related('subject', 'teacher'),
            many=True
        )

        return serializer.data

    def get_grade(self, obj):
        serializer = GradeInnerSerializer(obj.grade)

        return serializer.data
    
    def get_parents(self, obj):
        serializer = ParentInnerSerializer(obj.parent, many=True)

        return serializer.data



class PupilListSerializer(PupilBaseSerializer):
    parents = serializers.SerializerMethodField()

    grade = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'name_en', 'grade', 'average_mark', 'parents')

    def get_average_mark(self, obj):
        mark = DairyOfClass.objects.filter(pupil=obj).values_list('mark', flat=True)
        
        return obj.dairy_pupil.aggregate(average_mark=Avg('mark'))['average_mark'] if mark else 0

    def get_grade(self, obj):
        serializer = GradeInnerSerializer(obj.grade)
        
        return serializer.data

    def get_parents(self, obj):
        serializer = ParentInnerSerializer(obj.parent, many=True)

        return serializer.data


class PupilDefaultSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'username', 'grade', 'name_uz', 'name_ru', 'name_en')
