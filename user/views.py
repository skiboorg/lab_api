import json
import time

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from rest_framework import generics

from django.utils.timezone import now

import uuid

import logging
logger = logging.getLogger(__name__)



class UserUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        result = {'success': True}
        user = request.user
        data = request.data
        #print(data)
        if data.get('set_region'):
            print(data.get('region'))
            user.region_id = data.get('region')['id']
            user.save(update_fields=['region'])

        if data.get('set_dead_info'):

            user.dead_info = f"ФИО : {data.get('fio')} | ДР : {data.get('birtday')} | Контакты : {data.get('text')}"
            user.save(update_fields=['dead_info'])

        if data.get('update_use_in_yandex_services'):
            user.use_in_yandex_services = data.get('use_in_yandex_services')
            user.save(update_fields=['use_in_yandex_services'])

        if data.get('update_use_in_payback'):
            user.use_in_payback = data.get('use_in_payback')
            user.save(update_fields=['use_in_payback'])

        if data.get('avatar'):
            user.avatar = request.FILES.get('avatar')
            user.save(update_fields=['avatar'])
        if data.get('email'):
            check_email = User.objects.filter(email=data['email'])
            if check_email:
                result = {'success': False, 'message':'Такой email уже зарегистрирован'}
            else:
                user.email = data['email']
                user.save(update_fields=['email'])
        if data.get('password1'):
            user.set_password(data.get('password1'))
            user.save(update_fields=['password'])
        return Response(result, status=200)


class GetUser(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class AddUser(APIView):
    def post(self,request):
        raw_data = request.data['data']
        print(request.data)
        json_data = json.loads(raw_data)

        serializer = UserSerializer(data=json_data)
        print(request.FILES.get('image'))
        if serializer.is_valid():

            obj = serializer.save()
            obj.added_by = request.user
            if request.FILES.get('image'):
                obj.avatar = request.FILES.get('image')

            obj.save()
        else:
            print(serializer.errors)

        return Response(status=200)
class GetMyUsers(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        user = User.objects.get(uuid=self.request.query_params.get('id'))
        print(user)
        return User.objects.filter(added_by=user)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        result = False
        user = request.user
        if data['code'] == user.email_confirmation_code:
            user.set_password(data['password'])
            user.last_password_change = now()
            user.save()
            result = True
        return Response(result, status=200)


class SendConfirmCode(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # code = create_random_string(False, 6)
        # send_email.delay('Код подтверждения на сайте olftokenpro.com',
        #                  user.email, 'confirmation.html',
        #                  {'code': code}
        #                  )
        # user.email_confirmation_code = code
        user.save(update_fields=['email_confirmation_code'])
        logger.info(f'UID {user.id} {user.email} Send code on email')
        return Response(status=200)


class ActivateUser(APIView):
    def post(self, request):
        token = request.data.get('token')
        user = User.objects.get(email_confirmation_code=token)
        user.is_active = True
        user.email_confirmation_code = ''
        user.save(update_fields=["is_active", 'email_confirmation_code'])
        logger.info(f'UID {user.id} {user.email} Account is activated')
        return Response({'success': True}, status=200)



class UserRecoverPassword(APIView):
    def post(self, request):
        user = User.objects.get(email=request.data['email'])
        # password = create_random_string(False, num=8)
        # user.set_password(password)
        user.save()
        logger.info(f'UID {user.id} {user.email} recover password')
        # TODO .delay
        # send_email('Новый пароль на сайте ролф.рф',
        #            user.email,
        #            'notify.html',
        #            {"text": f"Ваш новый пароль : {password}"})
        return Response({'success': True}, status=200)


