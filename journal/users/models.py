# from django.db import models
# from django.contrib.auth.models import (
#     AbstractBaseUser,
#     BaseUserManager,
#     PermissionsMixin,
# )


# class NamedModel(models.Model):
#     name_uz = models.CharField(max_length=255)
#     name_ru = models.CharField(max_length=255, blank=True, null=True)
#     name_en = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         abstract = True


# class Role(NamedModel):
#     TEACHER = "Teacher"
#     STUDENT = "Student"
#     PARENT = "Parent"

#     USER_TYPE_CHOICES = [
#         (TEACHER, "Teacher"),
#         (STUDENT, "Student"),
#         (PARENT, "Parent")
#     ]

#     user_type = models.CharField(max_length=7, choices=USER_TYPE_CHOICES, default=STUDENT)

#     class Meta:
#         verbose_name = 'Role'
#         verbose_name_plural = 'Roles'

#     def __str__(self) -> str:
#         return self.user_type
    


# class UserManager(BaseUserManager):
#     def create_user(self, username, password=None, **extra_fields):
#         if username is None:
#             raise TypeError("username required to login")
#         if password is None:
#             raise TypeError("Password is required to login")
        
#         user = self.model(username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)

#         return user

#     def create_superuser(self, username, password):
#         if username is None:
#             raise TypeError("username is required to login")
#         if password is None:
#             raise TypeError("Password is required to login")
        
#         user = self.create_user(username=username, password=password)

#         user.is_superuser = True
#         user.is_staff = True
        
#         user.save(using=self._db)
        
#         return user
    

# class User(AbstractBaseUser, PermissionsMixin, NamedModel):
#     username = models.CharField(db_index=True, max_length=100, unique=True)
#     parent = models.ManyToManyField('self', symmetrical=True, blank=True, related_name='parent')
#     grade = models.ForeignKey('Grade', on_delete=models.SET_NULL, related_name='user_grade', null=True, blank=True)
#     children = models.ManyToManyField('self', symmetrical=True, blank=True, related_name='children')
#     role = models.ForeignKey(
#         Role,
#         on_delete=models.SET_NULL,
#         null=True, 
#         blank=True
#     )
    
#     is_staff = models.BooleanField(default=False)

#     objects = UserManager()

#     USERNAME_FIELD = "username"
#     REQUIRED_FIELDS = []

#     class Meta:
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'

#     def __str__(self):
#         return self.username