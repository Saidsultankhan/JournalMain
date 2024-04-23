from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from configs.models import User
from datetime import datetime
from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied


# class CustomTokenObtainPairView(TokenObtainPairView):

#     def post(self, request, *args, **kwargs):

#         username = request.data["username"]
#         user = User.objects.get(username=username)

#         if user is None:
#             raise PermissionDenied()

#         user.last_login = datetime.now()
#         user.save()

#         return super().post(request, *args, **kwargs)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("configs.urls")),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]


url_docs = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

urlpatterns += url_docs


# path('api/v1/auth/', include('djoser.urls')),
# path('auth/', include('djoser.urls.authtoken')),
# path('auth/', include('djoser.urls.jwt')),
# path('api-auth/', include('rest_framework.urls')),
# path('djoser/auth/', include('djoser.urls')),
