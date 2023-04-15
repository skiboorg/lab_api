
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction

from rest_framework import exceptions, serializers, status, generics
from .models import *
from djoser.conf import settings

from django.contrib.auth.tokens import default_token_generator


import logging
logger = logging.getLogger(__name__)


class SintezFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SintezFile
        fields = '__all__'

class SintezCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SintezCard
        fields = '__all__'


class SintezImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SintezImage
        fields = '__all__'


class SintezStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = SintezStep
        fields = '__all__'


class SintezSerializer(serializers.ModelSerializer):
    from user.serializers import UserSerializer
    worker = UserSerializer(many=False, required=False, read_only=True)
    cards = SintezCardSerializer(many=True, required=False, read_only=True)
    steps = SintezStepSerializer(many=True, required=False, read_only=True)
    images = SintezImageSerializer(many=True, required=False, read_only=True)
    files = SintezFileSerializer(many=True, required=False, read_only=True)
    image = serializers.ImageField(required=False, read_only=True)
    class Meta:
        model = Sintez
        fields = '__all__'

        extra_kwargs = {'image': {'required': False}}


class ProjectSerializer(serializers.ModelSerializer):
    sintezes = SintezSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Project
        fields = '__all__'














