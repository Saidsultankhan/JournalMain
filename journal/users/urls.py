from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include


router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
]
