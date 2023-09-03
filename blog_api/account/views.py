from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ChangePasswordSerializer, RegistrationSerializer, ActivationSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .permissions import IsActivePermission
from rest_framework.permissions import IsAuthenticated


User = get_user_model()


class RegistrationView(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Аккаунт успешно создан', status=201)
    

class ActivationView(APIView):

    def post(self, request):
        serializer = ActivationSerializer(
            data=request.data
        )
        if serializer.is_valid(raise_exception=True):
            serializer.activate()
            return Response(
                'Аккаунт успешно активирован',
                status=200
            )


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

class LogoutView(APIView):
    permission_classes = [IsActivePermission]

    def post(self, requests):
        user = requests.user
        Token.objects.filter(user=user).delete()
        return Response('Вы успешно вышли из своего аккаунта')
    

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data,context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('Пароль успешно обнавлен', status=200)

        
