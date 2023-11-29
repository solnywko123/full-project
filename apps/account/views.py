from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView

from config.tasks import send_confirmation_sms_task, send_confirmation_email_task
from .send_mail import send_confirmation_email
from .send_sms import sending_sms
from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()

class RegistrationView(APIView):  # регистрируем юзера
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            try:
                # send_confirmation_email(user.email, user.activation_code)
                send_confirmation_email_task(user.email, user.activation_code)


            except:
                return Response({"message": "Registered, but troubles with email", 'data': serializer.data}, status=201)
        return Response(serializer.data, status=201)


class UserListView(ListAPIView):  # получаем всех юзеров
    queryset = User.objects.all()
    serializers_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ActivationView(APIView):
    def get(self, request):
        code = request.GET.get('u')
        user = get_object_or_404(User, activation_code=code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Регистрация прошла успешно!!!', status=200)


# class ActivationFromNumberView(APIView):
#     def get(self, request):
#         phone_number = request.GET.get('phone_number')
#         user = get_object_or_404(User, phone_number=phone_number)
#         user.is_active = True
#         user.save()
#         # Отправить SMS с уведомлением о успешной активации по номеру телефона
#         sms_text = "Ваш аккаунт успешно активирован. Добро пожаловать!"
#         sending_sms(text=sms_text, receiver=phone_number)
#
#         return Response('Регистрация по номеру телефона прошла успешно!!!', status=200)


class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)


class RegistrationPhoneView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, requests):
        serializer = RegisterSerializer(data=requests.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # sending_sms(user.phone_number, user.activation_code)
            # sending_sms.delay(user.phone_number, user.activation_code)
            send_confirmation_sms_task(user.phone_number, user.activation_code)
            return Response('Succesfully registered', status=201)


class ActivationPhoneView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        code = request.data.get('activation_code')
        user = User.objects.filter(phone_number=phone, activation_code=code).first()
        if not user:
            return Response('No such user', status=400)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response('Succesfuly activated', status=200)
