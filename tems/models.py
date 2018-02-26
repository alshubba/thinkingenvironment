from django.db import models
from django.contrib.auth.models import User
from easy_thumbnails.fields import ThumbnailerImageField

class ThinkingEnvUser(User):
    USER_ROLES = (("admin","مدير"),("user","مستخدم"), ("expert","خبير"),)
    USER_SEX = (("male", "ذكر"), ("female", "أنثى"),)
    USER_MARITAL_STATUS = (("married", "متزوج"), ("single", "أعزب"),)
    role = models.CharField(max_length=255, default="user", choices=USER_ROLES)
    phone = models.CharField(max_length=255, null=True, blank=True)
    sex = models.CharField(max_length=255, null=True, blank=True, choices=USER_SEX)
    country = models.CharField(max_length=255, null=True, blank=True)
    city =  models.CharField(max_length=255, null=True, blank=True)
    neighborhood =  models.CharField(max_length=255, null=True, blank=True)
    marital_status =  models.CharField(max_length=255, null=True, blank=True, choices=USER_MARITAL_STATUS)
    forgot_password_token = models.CharField(max_length=255, null=True, blank=True)
    created_manually = models.BooleanField(default=False)
    booklet_download_count = models.IntegerField(default=0)

class Infographic(models.Model):
    title = models.CharField(max_length=255, default="")
    image = ThumbnailerImageField(upload_to='infographics/', null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Ticket(models.Model):
    TICKET_STATUS = (("open", "Open"),("closed", "Closed"),)
    title = models.CharField(max_length=255)
    body = models.TextField()
    status = models.CharField(max_length=255, choices=TICKET_STATUS, default="open")
    answer = models.TextField(null=True, blank=True)
    replier = models.IntegerField(null=True, blank=True) # id of the person who replied
    open_to_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(ThinkingEnvUser)

    def __str__(self):
        return self.title

class WorkshopRequest(models.Model):
    REQUEST_STATUS = (("open", "Open"), ("closed", "Closed"),)
    TRAINEES_SEX = (("male", "Male"), ("female", "Female"),("mixed", "Mixed"),)
    ABOUT_US_METHODS = (("social_media", "Social Media"), ("training_team", "Training Team"), ("people", "People"),("other","Other"),)
    status = models.CharField(max_length=255, choices=REQUEST_STATUS, default="open")
    is_workshop_direct = models.BooleanField(default=False)
    requesting_authority_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    neighborhood = models.CharField(max_length=255, null=True, blank=True)
    trainees_count = models.IntegerField()
    trainees_sex = models.CharField(max_length=255, choices=TRAINEES_SEX)
    director_phone_number = models.CharField(max_length=255)
    director_email = models.EmailField(max_length=255)
    date = models.DateTimeField()
    is_workshop_room_available = models.BooleanField(default=False)
    about_us = models.CharField(max_length=255, choices=ABOUT_US_METHODS)
    about_us_other_reason = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(ThinkingEnvUser)

    def __str__(self):
        return self.requesting_authority_name

class Workshop(models.Model):
    title = models.CharField(max_length=255)
    presenter = models.CharField(max_length=255)
    begin_date = models.DateTimeField()
    end_date = models.DateTimeField()
    price = models.IntegerField(default=0, null=True, blank=True)
    poster = models.ImageField(upload_to='workshops/', null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class WorkshopRegistration(models.Model):
    USER_SEX = (("male", "Male"), ("female", "Female"),)
    arabic_name = models.CharField(max_length=255)
    english_name = models.CharField(max_length=255)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    sex = models.CharField(max_length=255, choices=USER_SEX)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    workshop_evaluated = models.BooleanField(default=False)
    presenter_evaluated = models.BooleanField(default=False)
    organization_evaluated = models.BooleanField(default=False)
    user = models.ForeignKey(ThinkingEnvUser)
    workshop = models.ForeignKey(Workshop)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def require_evaluation(self):
        return self.workshop_evaluated or self.presenter_evaluated or self.organization_evaluated

    class Meta:
        unique_together = ['user', 'workshop']

    def __str__(self):
        return "{} | {}".format(self.english_name, self.workshop.title)

class WorkshopEvaluation(models.Model):
    EVALUATION_TYPES = (("workshop","البرنامج التدريبي"),("presenter","المدرب"),("organization","وحدة التدريب"))
    evaluation_type = models.CharField(max_length=255, choices=EVALUATION_TYPES)
    workshop_met_expectations = models.IntegerField(default=0)
    workshop_enough_duration = models.IntegerField(default=0)
    workshop_content = models.IntegerField(default=0)
    workshop_equipment_available = models.IntegerField(default=0)
    workshop_recommend_friends = models.IntegerField(default=0)
    presenter_on_time = models.IntegerField(default=0)
    presenter_on_topic = models.IntegerField(default=0)
    presenter_clear = models.IntegerField(default=0)
    presenter_suggestions_exchange = models.IntegerField(default=0)
    presenter_competent =models.IntegerField(default=0)
    organization_room_prepared = models.IntegerField(default=0)
    organization_organized = models.IntegerField(default=0)
    organization_cooperative = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(ThinkingEnvUser)
    workshop_registration = models.ForeignKey(WorkshopRegistration)
    workshop = models.ForeignKey(Workshop)

    def __str__(self):
        return "{} | {} | {}".format(self.user, self.workshop_registration.workshop.title, self.evaluation_type)

class AmbassadorRequest(models.Model):
    REQUEST_STATUS = (("open", "Open"), ("closed", "Closed"),)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    nationality = models.CharField(max_length=255)
    place_of_stay = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    about_you = models.TextField()
    what_can_you_provide = models.TextField()
    status = models.CharField(max_length=255, choices=REQUEST_STATUS, default="open")
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(ThinkingEnvUser)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    file = models.FileField(upload_to='books/', null=False)
    order = models.IntegerField(default=0)
    main_guide = models.BooleanField(default=False)
    training_guide = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class AmbassadorCountry(models.Model):
    name = models.CharField(max_length=255)
    main_representative = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class AmbassadorCity(models.Model):
    name = models.CharField(max_length=255)
    city_representative = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ambassador_country = models.ForeignKey(AmbassadorCountry)

    def __str__(self):
        return self.name

class AmbassadorExtraRepresentative(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    ambassador_city = models.ForeignKey(AmbassadorCity)

    def __str__(self):
        return self.name