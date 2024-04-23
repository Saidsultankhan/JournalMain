from rest_framework import serializers
from configs.models import ( 
    Grade,
    SubjectTeacher,
    User
)
from .dairy_of_class import TeacherInnerSerializer


class MentorInnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class SubjectTeacherInnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubjectTeacher
        fields = ('id', 'subject', 'teacher')



class GradeDetailSerializer(serializers.ModelSerializer):
    mentor = serializers.SerializerMethodField(source='teacher')
    name = serializers.CharField(source='__str__')
    pupils_number = serializers.SerializerMethodField()
    class_pupil = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = Grade
        fields = ('mentor', 'name', 'pupils_number', 'class_pupil', 'subjects')

    def get_parent_name_uz(self, parent_instance):

        return parent_instance.name_uz if parent_instance else None

    def get_class_pupil(self, obj):
        pupils_list = []
        
        for pupil in obj.user_grade.all():
            parents = []

            for parent in pupil.parent.values():
                parents.append(
                    {
                        'id': parent['id'],
                        'name_uz': parent['name_uz'],
                        'name_ru': parent['name_ru'],
                        'name_en': parent['name_en'],
                    }
                )

            pupils_list.append({
                'id': pupil.id,
                'name_uz': pupil.name_uz,
                'name_ru': pupil.name_ru,
                'name_en': pupil.name_en,
                'parents': parents
            })
        sorted_pupils = sorted(pupils_list, key=lambda x: x['name_uz'])

        numbered_pupils = [
            {
                **pupil_info,
                'number_in_dairy': idx + 1,
            } 
                for idx, pupil_info in enumerate(sorted_pupils)
        ]

        return numbered_pupils

    def get_pupils_number(self, obj):
        if obj.user_grade:
            return obj.user_grade.count()

    def get_mentor(self, obj):
        serializer = MentorInnerSerializer(obj.teacher)

        return serializer.data

    def get_subjects(self, obj):
        subject_teacher = SubjectTeacher.objects.filter(grade=obj).select_related('subject', 'teacher')            
        serializer = SubjectTeacherInnerSerializer(subject_teacher, many=True)

        return serializer.data
    

class GradeListSerializer(serializers.ModelSerializer):
    mentor = serializers.SerializerMethodField(source='teacher')
    name = serializers.CharField(source='__str__')
    pupils_number = serializers.SerializerMethodField()

    class Meta:
        model = Grade
        fields = ('id', 'mentor', 'name', 'pupils_number')

    def get_pupils_number(self, obj):
        if obj.user_grade:
            return obj.user_grade.count()

    def get_mentor(self, obj):
        serializer = TeacherInnerSerializer(obj.teacher)

        return serializer.data
    

class GradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = '__all__'
        