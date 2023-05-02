from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
from user import serializer as user_serializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class LoginView(KnoxLoginView):
    permission_classes = [permissions.AllowAny, ]

    def get_user_serializer_class(self):
        return user_serializer.UserSerializer

    @csrf_exempt
    def post(self, request, format=None):  # NOQA
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class GetUserDetailsView(APIView):
    def get(self, request):
        return Response(user_serializer.UserSerializer(instance=self.request.user).data)
