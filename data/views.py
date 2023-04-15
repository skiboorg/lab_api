import json
import time
from decimal import Decimal

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


class GetProjects(generics.ListAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        from user.models import User
        user = User.objects.get(uuid=self.request.query_params.get('id'))
        return Project.objects.filter(owners__in=[user])


class GetProject(generics.RetrieveAPIView):
    serializer_class = ProjectSerializer
    def get_object(self):

        return Project.objects.get(uuid=self.request.query_params.get('id'))

class AddSintez(APIView):
    def post(self,request):
        raw_data = request.data['data']
        json_data = json.loads(raw_data)
        print(json_data)
        serializer = SintezSerializer(data=json_data)
        if serializer.is_valid():
            print('good')
            sintez = serializer.save()
            proj = Project.objects.get(uuid=json_data['project_uuid'])
            sintez.image = request.FILES.get('image')
            sintez.project = proj
            sintez.worker = request.user
            sintez.hours = Decimal(json_data['hours'])
            sintez.save()
            sintez.project.total_hours += sintez.hours
            sintez.project.save()
            start_card_serializer = SintezCardSerializer(data=json_data['start_card'])
            if start_card_serializer.is_valid():
                card = start_card_serializer.save()
                card.sintez = sintez
                card.save()
            else:
                print(start_card_serializer.errors)
            last_index = 0
            for index,card in enumerate(json_data['cards']):
                card_serializer = SintezCardSerializer(data=card)
                if card_serializer.is_valid():
                    card = card_serializer.save()
                    card.sintez = sintez
                    card.order_num = index + 2
                    card.save()
                    last_index = index + 2
                else:
                    print('card_serializer', card_serializer.errors)
            final_card_serializer = SintezCardSerializer(data=json_data['final_card'])
            if final_card_serializer.is_valid():
                card = final_card_serializer.save()
                card.sintez = sintez
                card.order_num = last_index + 1
                card.save()
            else:
                print('final_card_serializer',final_card_serializer.errors)

            # for index, step in enumerate(json_data['steps']):
            #     try:
            #         SintezStep.objects.create(sintez=sintez, text=step['text'],image=request.FILES.getlist('step_images')[index])
            #     except:
            #         SintezStep.objects.create(sintez=sintez,text=step['text'])
            #
            # for index, img in enumerate(json_data['images']):
            #     try:
            #         SintezImage.objects.create(sintez=sintez, text=img['text'],image=request.FILES.getlist('images_images')[index])
            #     except:
            #         break
            #
            # for index, file in enumerate(json_data['files']):
            #     try:
            #         SintezFile.objects.create(sintez=sintez, text=file['text'],file=request.FILES.getlist('files_images')[index])
            #     except:
            #         break

        else:
            print(serializer.errors)
        # print(json_data)
        # print(request.FILES.getlist('step_images'))
        # print(request.FILES.getlist('images_images'))
        # print(request.FILES.getlist('files_images'))
        # print(json_data['steps'])
        # for index, step in enumerate(json_data['steps']):

        return Response(status=200)
class AddProject(APIView):
    def post(self,request):
        from user.models import User
        raw_data = request.data['data']
        json_data = json.loads(raw_data)
        serializer = ProjectSerializer(data=json_data)
        print(json_data['selectedUsers'])

        if serializer.is_valid():
            obj = serializer.save()
            if request.FILES.get('image'):
                obj.image = request.FILES.get('image')
                obj.save()
            obj.owners.add(request.user)
            for user in json_data['selectedUsers']:
                user = User.objects.get(uuid=user['uuid'])
                obj.owners.add(user)
        else:
            print(serializer.errors)

        return Response(status=200)



class GetSintez(generics.RetrieveAPIView):
    serializer_class = SintezSerializer
    def get_object(self):

        return Sintez.objects.get(uuid=self.request.query_params.get('id'))



