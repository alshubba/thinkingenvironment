from django.conf.urls import include, url
from rest_framework import routers
from push_notifications.api.rest_framework import APNSDeviceAuthorizedViewSet, GCMDeviceAuthorizedViewSet
from . import views, api

router = routers.DefaultRouter()
router.register(r'v1/users', api.UserViewSet)
router.register(r'v1/infographics', api.InfographicViewSet)
router.register(r'v1/tickets', api.TicketViewSet)
router.register(r'v1/workshop_requests', api.WorkshopRequestViewSet)
router.register(r'v1/workshops', api.WorkshopViewSet)
router.register(r'v1/workshop_registrations', api.WorkshopRegistrationViewSet)
router.register(r'v1/workshop_evaluations', api.WorkshopEvaluationViewSet)
router.register(r'v1/ambassador_requests', api.AmbassadorRequestViewSet)
router.register(r'v1/device/apns', APNSDeviceAuthorizedViewSet)
router.register(r'v1/device/gcm', GCMDeviceAuthorizedViewSet)



urlpatterns = [
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^forgot_password/(?P<token>[\w\-]+)/$', views.forgot_password, name='forgot_password'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^tickets/$', views.ticket_list, name="ticket_list"),
    url(r'^tickets/(?P<pk>\d+)/$', views.ticket_detail, name='ticket_detail'),
    url(r'^tickets/(?P<pk>\d+)/edit$', views.ticket_edit, name='ticket_edit'),
    url(r'^workshops/$', views.workshop_list, name="workshop_list"),
    url(r'^workshops/(?P<pk>\d+)/$', views.workshop_detail, name='workshop_detail'),
    url(r'^workshops/add/$', views.workshop_add, name='workshop_add'),
    url(r'^workshops/(?P<pk>\d+)/edit/$', views.workshop_edit, name='workshop_edit'),
    url(r'^workshops/(?P<pk>\d+)/delete/$', views.workshop_delete, name='workshop_delete'),
    url(r'^workshop_registrations/(?P<pk>\d+)/delete/$', views.workshop_registration_delete, name='workshop_registration_delete'),
    url(r'^workshop_requests/$', views.workshop_requests_list, name="workshop_requests_list"),
    url(r'^workshop_requests/(?P<pk>\d+)/$', views.workshop_request_detail, name='workshop_requests_detail'),
    url(r'^workshop_requests/(?P<pk>\d+)/change_status$', views.change_workshop_request_status, name='change_workshop_request_status'),
    url(r'^infographics/$', views.infographic_list, name="infographic_list"),
    url(r'^infographics/add/$', views.infographic_add, name='infographic_add'),
    url(r'^infographics/(?P<pk>\d+)/delete/$', views.infographic_delete, name='infographic_delete'),
    url(r'^ambassador_requests/$', views.ambassador_requests_list, name="ambassador_requests_list"),
    url(r'^ambassador_requests/(?P<pk>\d+)/$', views.ambassador_request_detail, name='ambassador_requests_detail'),
    url(r'^ambassador_requests/(?P<pk>\d+)/change_status$', views.change_ambassador_request_status, name='change_ambassador_request_status'),
    url(r'^workshop_evaluations/$', views.workshop_evaluations_list, name="workshop_evaluations_list"),
    url(r'^workshop_evaluations/(?P<pk>\d+)/$', views.workshop_evaluation_detail, name='workshop_evaluation_detail'),
    url(r'^api/', include(router.urls, namespace="api")),
    url(r'api/v1/get_user', api.RetrieveUserByToken.as_view()),
    url(r'api/v1/check_email', api.RetrieveUserByEmail.as_view()),
]



















