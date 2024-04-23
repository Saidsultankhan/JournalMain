from rest_framework import serializers
from configs.models import Homework, SubjectTeacher, Role, User, StaticChoices
from pprint import pprint
from rest_framework.exceptions import PermissionDenied


class HomeworkDefaultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Homework
        fields = (
            "created_at",
            "deadline",
            "task_file",
            "student_answer",
            "status",
            "student",
        )


class HomeworkCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Homework
        exclude = ("teacher", "mark", "student_answer", "status")

    def create(self, validated_data):
        print(2)
        teacher_creater = self.context["request"].user

        if teacher_creater.role.user_type == Role.TEACHER:
            teacher = teacher_creater

        validated_data.pop("teacher", [])
        validated_data.get("status", [])
        status = StaticChoices.ASSIGNED
        student = validated_data.get('student', [])
        print()
        teachers = SubjectTeacher.objects.filter(teacher=teacher_creater, grade=student.grade)
        print(teachers)

        data = Homework.objects.create(**validated_data, teacher=teacher, status=status)

        return data


class HomeworkStudentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Homework
        fields = ("student_answer",)

    def update(self, instance, validated_data):
        print("sss")
        instance.student_answer = validated_data.get(
            "student_answer", instance.student_answer
        )

        created_at = instance.created_at
        deadline = instance.deadline
        difference = deadline - created_at

        if difference.seconds <= 0:
            instance.mark = 2
            instance.status = StaticChoices.MARKED

        if not instance.status == StaticChoices.MARKED:
            instance.status = StaticChoices.SUBMITTED

        instance.save()

        return instance


class HomeworkTeacherUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Homework
        fields = ("mark",)

        def update(self, instance, validated_data):
            status = validated_data.get("status", instance.status)

            if not status == StaticChoices.SUBMITTED:
                raise PermissionDenied("Сперва студент должен загрузить ответ")
            
            mark = validated_data.get("mark", [])

            if mark:
                raise PermissionDenied(
                    "Ученик просрочил deadline, его оценка автоматически была зафиксирована"
                )

            instance.mark = validated_data.get("mark", [])
            instance.save()

            return instance
