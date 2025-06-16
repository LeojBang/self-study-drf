from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from authentication.apps import AuthenticationConfig
from authentication.views import UserViewSet

app_name = AuthenticationConfig.name
router = SimpleRouter()
router.register("register", UserViewSet, basename="register")

urlpatterns = [
    path(
        "login/",
        TokenObtainPairView.as_view(),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
urlpatterns += router.urls
