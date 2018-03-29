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
router.register(r'v1/books', api.BookViewSet)
router.register(r'v1/ambassador_list', api.AmbassadorCountryViewSet)
router.register(r'v1/device/apns', APNSDeviceAuthorizedViewSet)
router.register(r'v1/device/gcm', GCMDeviceAuthorizedViewSet)



urlpatterns = [
    url(r'^$', views.main_view, name="main"),
    url(r'^contact_us/$', views.contact_us, name='contact_us'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^forgot_password/(?P<token>[\w\-]+)/$', views.forgot_password, name='forgot_password'),
    url(r'^forgot_password_success/$', views.forgot_password_success, name='forgot_password_success'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^profile/$', views.profile, name="profile"),
    url(r'^profile/edit/$', views.profile_edit, name="profile_edit"),
    url(r'^profile/password/$', views.profile_password, name="profile_password"),
    url(r'^users/$', views.user_list, name="user_list"),
    url(r'^user_add/$', views.user_add, name="user_add"),
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
    url(r'^books/$', views.book_list, name="book_list"),
    url(r'^books/add$', views.book_add, name="book_add"),
    url(r'^books/(?P<pk>\d+)/edit/$', views.book_edit, name='book_edit'),
    url(r'^books/(?P<pk>\d+)/delete/$', views.book_delete, name='book_delete'),
    url(r'^ambassador_countries/$', views.ambassador_country_list, name="ambassador_country_list"),
    url(r'^ambassador_countries/add$', views.ambassador_country_add, name="ambassador_country_add"),
    url(r'^ambassador_countries/(?P<pk>\d+)/edit/$', views.ambassador_country_edit, name='ambassador_country_edit'),
    url(r'^ambassador_countries/(?P<pk>\d+)/delete/$', views.ambassador_country_delete, name='ambassador_country_delete'),
    url(r'^ambassador_countries/(?P<pk>\d+)/$', views.ambassador_country_detail, name='ambassador_country_detail'),
    url(r'^ambassador_countries/(?P<country_pk>\d+)/city/(?P<city_pk>\d+)/$', views.ambassador_city_detail, name='ambassador_city_detail'),
    url(r'^ambassador_countries/(?P<country_pk>\d+)/city/(?P<city_pk>\d+)/edit/$', views.ambassador_city_edit, name='ambassador_city_edit'),
    url(r'^ambassador_countries/(?P<country_pk>\d+)/city/(?P<city_pk>\d+)/delete/$', views.ambassador_city_delete, name='ambassador_city_delete'),
    url(r'^api/', include(router.urls, namespace="api")),
    url(r'api/v1/get_user', api.RetrieveUserByToken.as_view()),
    url(r'api/v1/check_email', api.RetrieveUserByEmail.as_view()),
    url(r'api/v1/increase_download_count', api.IncreaseUserDownloadCount.as_view()),
    url(r'api/v1/training_book', api.TrainingBooklet.as_view()),
    url(r'api/v1/email_book', api.SendBookLinkEmail.as_view())
]



















