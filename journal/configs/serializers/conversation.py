from rest_framework import serializers
from configs.models import Conversation, StaticChoices, Role, SubjectTeacher
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import AuthenticationFailed


class ConversationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conversation
        fields = "__all__"

    def create(self, validated_data):
        current_user = self.context["request"].user
        coming_user = validated_data["participant"][0]

        # subject_teacher_parents = current_user.subject_teacher_teacher
        # subjects_teacher_parents = SubjectTeacher.objects.filter(teacher=current_user, grade=)

        
        if (
            current_user.role.user_type == Role.STUDENT
            or coming_user.role.user_type == Role.STUDENT
        ):
            raise ValueError("Ученик не может чатиться!")

        if validated_data["chat_type"] == StaticChoices.PERSONAL:
            
            if len(validated_data["participant"]) != 1:
                raise ValueError("Количество участников в личном чате должно быть 2!.")

            if current_user.role.user_type == Role.PARENT:
                mentors = current_user.parent.filter(grade__teacher=coming_user).exists()
                subjects_teachers = current_user.children.filter(
                    grade__subject_teacher_class__teacher=coming_user
                ).exists()

                if not mentors or subjects_teachers:
                    raise PermissionError(
                        "Вы можете писать только преподавателям ваших детей!"
                    )

            elif current_user.role.user_type == Role.TEACHER:
                parents = current_user.class_teacher.user_grade.filter(
                    parent=coming_user
                ).exists()
                if not parents:
                    raise PermissionError(
                        "Вы можете общаться только с родителями ваших учеников!"
                    )

            user_conversations = Conversation.objects.filter(participant=current_user)

            if user_conversations.filter(participant=coming_user).exists():
                raise ValueError("Чат между вами уже существует!")

        elif validated_data["chat_type"] == StaticChoices.GROUP:
            user_ids = [user.id for user in validated_data["participant"]]
            user_roles = Role.objects.filter(user_role__id__in=user_ids).values_list(
                "user_type", flat=True
            )

            if Role.STUDENT in user_roles:
                raise ValueError("Ученик не может чатиться!")

        participants_data = validated_data.pop("participant", [])
        participants_data.insert(0, current_user)
        conversation = Conversation.objects.create(**validated_data)

        conversation.participant.add(*participants_data)
        
        return conversation
