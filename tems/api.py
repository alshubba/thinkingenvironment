from datetime import datetime
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template import loader
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
            email_body = loader.render_to_string("tems/email_forgot_password.html",{"user":user})
            send_mail("تطبيق البيئة المعززة للتفكير - إعادة إنشاء كلمة المرور", "", "Thinking Environment", [user.email], False,
                      None, None, None, email_body)
            models.AuditLog.objects.create(title="email_sent",
                                           event="sent a forgot-password email to user {}".format(user.username),
                                           user=user)
            return Response({"result": "success"})
        return Response({"result": "error - user does not exist"})


class IncreaseUserDownloadCount(views.APIView):
    def post(self, request, format=None):
        user = models.ThinkingEnvUser.objects.get(username=request.user)
        count = user.booklet_download_count
        user.booklet_download_count = count + 1
        user.save()
        return Response({"result": "success"})


class SendBookLinkEmail(views.APIView):
    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'POST'
                else IsAuthenticated()),

    def post(self, request, format=None):
        email = request.data.get('email', None)
        id = request.data.get('id', None)
        if id == None:
            return Response({"result": "error - id not provided"})
        book = get_object_or_404(models.Book, id=id)
        if book != None:
            email_title = "تطبيق البيئة المعززة للتفكير - {}".format(book.title)
            email_body = loader.render_to_string("tems/email_send_book_link.html", {"book":book})
            send_mail(email_title, "", "Thinking Environment", [email], False,
                      None, None, None, email_body)
            """
            models.AuditLog.objects.create(title="email_sent",
                                           event="sent an email with a link to book {} to email {}".format(book.title, email),
                                           user=request.user)
            
            if book.main_guide:
                count = user.main_booklet_email_count
                user.main_booklet_email_count = count + 1
                user.date_main_booklet_email_sent = datetime.now()
                user.save()
            """
            return Response({"result": "success"})
        return Response({"result": "error - book does not exist"})


class TrainingBooklet(views.APIView):
    def get(self, request, format=None):
        books = models.Book.objects.filter(training_guide=True)
        if not books:
            return Response({})
        else:
            book = models.Book.objects.get(training_guide=True)
            serializer = serializers.BookSerializer(book)
            return Response(serializer.data)


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

    def create(self, validated_data):
        response = super(TicketViewSet, self).create(validated_data)
        managers = models.ThinkingEnvUser.objects.filter(role="expert")
        ticket = models.Ticket.objects.get(pk=response.data["id"])
        emails = []
        if managers:
            for m in managers:
                emails.append(m.email)
        email_body = loader.render_to_string("tems/email_new_ticket.html", {"ticket": ticket})
        send_mail("تطبيق البيئة المعززة للتفكير - إستشارة جديدة", "", "Thinking Environment",
                  emails, False,
                  None, None, None, email_body)

        return response

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
    queryset = models.Book.objects.filter(training_guide=False)
    serializer_class = serializers.BookSerializer

class AmbassadorCountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.AmbassadorCountry.objects.all()
    serializer_class = serializers.AmbassadorCountrySerializer

class ExpertViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Expert.objects.all()
    serializer_class = serializers.ExpertSerializer