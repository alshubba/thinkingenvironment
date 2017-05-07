from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.decorators import authentication_classes
from rest_framework.response import Response

from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ThinkingEnvUser
        fields = ('id', 'username', 'password', 'email','first_name', 'last_name', 'phone', 'country', 'city', 'neighborhood', 'sex', 'marital_status')
        extra_kwargs = {'password': {'write_only': True}}

    @authentication_classes([])
    def create(self, validated_data):
        user = models.ThinkingEnvUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        response = super(UserSerializer, self).update(instance, validated_data)
        password = validated_data.get('password')
        if password != None:
            instance.set_password(password)
            instance.save()
        return response

class InfographicSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = models.Infographic
        fields = ('id', 'title', 'url')

    def get_url(self,obj):
        return obj.image.url

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ticket
        fields = ('id', 'title', 'body', 'status', 'answer', 'replier', 'open_to_public', 'created_at','user')

class WorkshopRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WorkshopRequest
        fields = '__all__'

class WorkshopSerializer(serializers.ModelSerializer):
    poster_url = serializers.SerializerMethodField()

    class Meta:
        model = models.Workshop
        fields = ('id', 'title', 'presenter', 'begin_date', 'end_date', 'price', 'poster_url', 'created_at')

    def get_poster_url(self,obj):
        return obj.poster.url

class WorkshopRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WorkshopRegistration
        fields = '__all__'

class WorkshopRegistrationUserSerializer(serializers.ModelSerializer):
    workshop = WorkshopSerializer()
    class Meta:
        model = models.WorkshopRegistration
        fields = '__all__'

class WorkshopEvaluationSerializer(serializers.ModelSerializer):
    #workshop_registration = WorkshopRegistrationSerializer()

    class Meta:
        model = models.WorkshopEvaluation
        fields = '__all__'

class AmbassadorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AmbassadorRequest
        fields = '__all__'