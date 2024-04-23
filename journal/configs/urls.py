from django.urls import path, include
from rest_framework.routers import DefaultRouter
from configs.views import (
    GradeViewSet,
    TeacherViewSet,
    DairyViewSet,
    PupilsViewSet,
    PDFGeneratorView,
    ExcelGenerateViewSet,
    WordToPDFView,
    SubjectTeacherViewSet,
    ConversationViewSet,
    MessageViewSet,
    UserModelViewset,
    HomeworkViewSet
)
from configs.models import User
from datetime import datetime

    

router = DefaultRouter()

router.register(r'class', GradeViewSet)
router.register(r'user', UserModelViewset)
router.register(r'dairy', DairyViewSet)
router.register(r'teacher', TeacherViewSet)
router.register(r'pupil', PupilsViewSet)
router.register(r'subject_teacher', SubjectTeacherViewSet, basename='subject-teacher')
router.register(r'conversation', ConversationViewSet, basename='conversation')
router.register(r'message', MessageViewSet,  basename='message')
router.register(r'homework', HomeworkViewSet, basename='homework')


urlpatterns = [
    path('', include(router.urls)),
    path('pdf/', PDFGeneratorView.as_view(), name='download_pdf'),
    path('excel/', ExcelGenerateViewSet.as_view(), name='download_excel'),
    path('word-to-pdf/', WordToPDFView.as_view(), name='word_to_pdf'),
]


urlpatterns += router.urls



# SubjectViewSet,
# UserViewSet,
# ParentsViewSet,
# router.register(r'parents', ParentsViewSet)
# router.register(r'subjects', SubjectViewSet)
# router.register(r'unused_users_list', UserViewSet, basename='user')