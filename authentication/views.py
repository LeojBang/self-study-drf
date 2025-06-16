from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from authentication.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
