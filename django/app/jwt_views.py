from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class EmployeeTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Accept employee number + password for JWT login (Angular sends `enumber`)."""

    username_field = "enumber"


class EmployeeTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmployeeTokenObtainPairSerializer
