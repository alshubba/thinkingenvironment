from datetime import datetime
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import views, viewsets, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import uuid

from . import models
from . import serializers

class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated()

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        user = models.ThinkingEnvUser.objects.get(username=request.data["username"])
        serializer = serializers.UserSerializer(user)
        token = response.data['token']
        return Response({'token': token, 'user': serializer.data})

class RetrieveUserByToken(views.APIView):
    def get(self, request, format=None):
        user = models.ThinkingEnvUser.objects.get(username=request.user)
        serializer = serializers.UserSerializer(user)
        return Response({"user": serializer.data})

class RetrieveUserByEmail(views.APIView):
    def get_permissions(self):
        return (AllowAny() if self.request.method == 'POST'
                else IsAuthenticated()),

    def post(self, request, format=None):
        email = request.data.get('email',None)
        if email == None:
            return Response({"result": "error - email not provided"})
        user = get_object_or_404(models.ThinkingEnvUser, email = email)
        if user != None:
            user.forgot_password_token = str(uuid.uuid4())
            user.save()
            return Response({"result": "success"})
        return Response({"result": "error - user does not exist"})


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.ThinkingEnvUser.objects.all()
    serializer_class = serializers.UserSerializer

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'POST'
                else IsAuthenticated()),

    def create(self, request, *args, **kwargs):
        email = request.data['email']
        try:
            user_email = models.ThinkingEnvUser.objects.get(email = email)
        except models.ThinkingEnvUser.DoesNotExist:
            user_email = None
        if user_email != None:
            return Response({"email": ["email exists"]})
        return super(UserViewSet, self).create(request, *args, **kwargs)

    @detail_route(methods=['get'])
    def tickets(self, request, pk=None):
        user = self.get_object()
        serializer = serializers.TicketSerializer(
            user.ticket_set.all(), many=True
        )
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def workshopRegistrations(self, request, pk=None):
        user = self.get_object()
        serializer = serializers.WorkshopRegistrationUserSerializer(
            user.workshopregistration_set.all(), many=True
        )
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def workshopsRequireEvaluation(self, request, pk=None):
        user = self.get_object()
        """
        Q(end_date__gte=datetime.now()) &
                                                         Q(workshop_evaluated = False) |
                                                         Q(presenter_evaluated = False) |
                                                         Q(organization_evaluated = False)
                                                         """
        workshops = user.workshopregistration_set.filter(Q(workshop__end_date__lte=datetime.now())&
                                                         (Q(workshop_evaluated=False) |
                                                         Q(presenter_evaluated=False) |
                                                         Q(organization_evaluated=False))
                                                         )
        serializer = serializers.WorkshopRegistrationUserSerializer(
            workshops, many=True
        )
        return Response(serializer.data)


class InfographicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Infographic.objects.all()
    serializer_class = serializers.InfographicSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = models.Ticket.objects.all()
    serializer_class = serializers.TicketSerializer

    @list_route()
    def public(self, request):
        tickets = models.Ticket.objects.filter(open_to_public=True)
        serializer = serializers.TicketSerializer(
            tickets, many=True
        )
        return Response(serializer.data)

class WorkshopRequestViewSet(viewsets.ModelViewSet):
    queryset = models.WorkshopRequest.objects.all()
    serializer_class = serializers.WorkshopRequestSerializer

class WorkshopViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Workshop.objects.all()
    serializer_class = serializers.WorkshopSerializer

    @list_route()
    def current(self,request):
        workshops = models.Workshop.objects.filter(end_date__gte=datetime.now())
        serializer = serializers.WorkshopSerializer(
            workshops, many=True
        )
        return Response(serializer.data)

class WorkshopRegistrationViewSet(viewsets.ModelViewSet):
    queryset = models.WorkshopRegistration.objects.all()
    serializer_class = serializers.WorkshopRegistrationSerializer


class WorkshopEvaluationViewSet(viewsets.ModelViewSet):
    queryset = models.WorkshopEvaluation.objects.all()
    serializer_class = serializers.WorkshopEvaluationSerializer

    def create(self, validated_data):
        response = super(WorkshopEvaluationViewSet, self).create(validated_data)
        workshop_registration = models.WorkshopRegistration.objects.get(pk=response.data['workshop_registration'])
        evaluation_type = response.data['evaluation_type']
        if evaluation_type == "workshop":
            workshop_registration.workshop_evaluated = True
        elif evaluation_type == "presenter":
            workshop_registration.presenter_evaluated = True
        elif evaluation_type == "organization":
            workshop_registration.organization_evaluated = True
        workshop_registration.save()
        return response


class AmbassadorRequestViewSet(viewsets.ModelViewSet):
    queryset = models.AmbassadorRequest.objects.all()
    serializer_class = serializers.AmbassadorRequestSerializer

class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer