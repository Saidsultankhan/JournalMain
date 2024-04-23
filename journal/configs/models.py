from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError


class NamedModel(models.Model):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255, blank=True, null=True)
    name_en = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True


class StaticChoices:

    QUARTER_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    )

    MARK_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    SENT = "Sent"
    SEEN = "Seen"

    STATUS_MESSAGE_CHOICES = ((SENT, "Sent"), (SEEN, "Seen"))

    TYPE_CHOICES = (
        ("a", "a"),
        ("б", "б"),
        ("в", "в"),
        ("г", "г"),
        ("д", "д"),
    )

    ASSIGNED = "Assigned"
    SUBMITTED = "Submitted"
    MARKED = "Marked"

    STATUS_TASK_CHOICES = [
        (ASSIGNED, "Assigned"),
        (SUBMITTED, "Submitted"),
        (MARKED, "Marked"),
    ]

    PERSONAL = "Personal"
    GROUP = "Group"

    CHAT_TYPE_CHOICES = (
        (PERSONAL, "Personal"),
        (GROUP, "Group"),
    )


class Role(NamedModel):
    TEACHER = "Teacher"
    STUDENT = "Student"
    PARENT = "Parent"

    USER_TYPE_CHOICES = [(TEACHER, "Teacher"), (STUDENT, "Student"), (PARENT, "Parent")]

    user_type = models.CharField(
        max_length=7, choices=USER_TYPE_CHOICES, default=STUDENT
    )

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self) -> str:
        return self.user_type


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if username is None:
            raise TypeError("username required to login")
        if password is None:
            raise TypeError("Password is required to login")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password):
        if username is None:
            raise TypeError("username is required to login")
        if password is None:
            raise TypeError("Password is required to login")

        user = self.create_user(username=username, password=password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin, NamedModel):
    username = models.CharField(db_index=True, max_length=100, unique=True)
    parent = models.ManyToManyField("self", symmetrical=True, blank=True)
    grade = models.ForeignKey(
        "Grade",
        on_delete=models.SET_NULL,
        related_name="user_grade",
        null=True,
        blank=True,
    )
    children = models.ManyToManyField("self", symmetrical=True, blank=True)
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, blank=True, related_name="user_role"
    )

    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username


class DairyOfClass(models.Model):
    mark = models.PositiveSmallIntegerField(choices=StaticChoices.MARK_CHOICES)
    pupil = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="dairy_pupil",
        null=True,
        blank=True,
    )

    subject = models.ForeignKey(
        "Subject", related_name="subject", on_delete=models.CASCADE
    )

    quarter = models.PositiveSmallIntegerField(choices=StaticChoices.QUARTER_CHOICES)
    grade = models.ForeignKey(
        "Grade",
        on_delete=models.SET_NULL,
        related_name="dairy_of_class",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Dairy"
        verbose_name_plural = "Dairies"

    def __str__(self):
        return f"{self.mark}"


class Grade(models.Model):
    number = models.SmallIntegerField()
    type = models.CharField(max_length=1, choices=StaticChoices.TYPE_CHOICES)
    teacher = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        related_name="class_teacher",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        unique_together = ("number", "type")

    def __str__(self):
        return f"{self.number}{self.type}"


class Subject(NamedModel):

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.name_en


class SubjectTeacher(models.Model):
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subject_teacher_teacher"
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="subject_teacher_subject"
    )
    grade = models.ForeignKey(
        Grade, on_delete=models.CASCADE, related_name="subject_teacher_class"
    )

    def __str__(self):
        return f"{self.subject} - {self.teacher}"

    class Meta:
        verbose_name = "Subject-Teacher"
        verbose_name_plural = "Subjects-Teachers"


class Homework(models.Model):
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="set_homeworks"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    mark = models.PositiveSmallIntegerField(
        choices=StaticChoices.MARK_CHOICES, null=True, blank=True
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assigned_homeworks"
    )
    task_file = models.FileField(upload_to="homework_tasks/")
    student_answer = models.FileField(
        upload_to="student_answers/", null=True, blank=True
    )
    status = models.CharField(
        max_length=10, choices=StaticChoices.STATUS_TASK_CHOICES, default="assigned"
    )

    class Meta:
        verbose_name = "Homework"
        verbose_name_plural = "Homeworks"

    def __str__(self):
        return f"Homework assigned by {self.teacher.username} at {self.created_at}"

    def save(self, *args, **kwargs):
        # Преобразовать дату deadline в часовой пояс 'Asia/Tashkent'
        if self.deadline and self.deadline.tzinfo is None:
            # Получаем объект временной зоны для 'Asia/Tashkent'
            tz = timezone.pytz.timezone('Asia/Tashkent')
            # Преобразуем дату и время в часовой пояс 'Asia/Tashkent'
            self.deadline = self.deadline.astimezone(tz)
        super().save(*args, **kwargs)


class Conversation(models.Model):
    chat_type = models.CharField(max_length=20, choices=StaticChoices.CHAT_TYPE_CHOICES)
    participant = models.ManyToManyField(User)

    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"

    def __str__(self):
        if self.chat_type == StaticChoices.PERSONAL:
            participants = self.participant.all()
            if self.participant.count() == 2:
                usernames = [participant.username for participant in participants]
                return f"Личный чат: {usernames[0]} - {usernames[1]}"
            else:
                return "Личный чат (несколько участников)"
        elif self.chat_type == StaticChoices.GROUP:
            return f"Групповой чат: {self.id}"
        else:
            return f"Неизвестный тип чата: {self.chat_type}"


class Message(models.Model):
    text = models.CharField(
        max_length=255, null=False, blank=False, default="default-text"
    )
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, null=True, blank=True
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_changed = models.BooleanField(default=False)
    status = models.CharField(
        max_length=10,
        choices=StaticChoices.STATUS_MESSAGE_CHOICES,
        default=StaticChoices.SENT,
    )
    viewed_at = models.DateTimeField(default=None, null=True, blank=True)
    reply_id = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, default=None
    )

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return str(self.id)
