from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from push_notifications.models import APNSDevice, GCMDevice

from . import forms, models

def forgot_password(request,token):
    user = get_object_or_404(models.ThinkingEnvUser, forgot_password_token = token)
    if request.method == "POST":
        password = request.POST["password"]
        repeat_password = request.POST["repeat-password"]
        if password != repeat_password:
            messages.error(request, "اسم  المستخدم  أو  كلمة  المرور  غير  صحيح")
        else:
            user.set_password(password)
            user.forgot_password_token = ""
            user.save()
            messages.success(request, "تمت تغيير كلمة السر بنجاح")
            return HttpResponseRedirect("/tems/forgot_password_success")
    return render(request, "tems/forgot_password.html")

def forgot_password_success(request):
    return render(request, "tems/forgot_password_success.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            teUser = models.ThinkingEnvUser.objects.get(username=user.username)
            if (teUser.role == "admin") or (teUser.role == "expert"):
                login(request, user)
                return HttpResponseRedirect("/tems/dashboard")
            else:
                messages.error(request, "عذرا  ولكن  هذه  الصفحة  مخصصة  فقط  للمدراء  والخبراء")
        else:
            messages.error(request, "اسم  المستخدم  أو  كلمة  المرور  غير  صحيح")
    if request.user.is_authenticated:
        return HttpResponseRedirect("/tems/dashboard")
    return render(request, 'tems/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/tems/login")

@login_required
def dashboard(request):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    users_count = models.ThinkingEnvUser.objects.count()
    tickets_count = models.Ticket.objects.filter(status="open").count()
    workshops_count = models.Workshop.objects.count()
    infographics_count = models.Infographic.objects.count()
    workshop_requests_count = models.WorkshopRequest.objects.filter(status="open").count()
    ambassadors_count = models.AmbassadorRequest.objects.filter(status="open").count()
    workshop_evaluations_count = models.WorkshopEvaluation.objects.count()
    return render(request, 'tems/dashboard.html', {"user": te_user,
                                                   "users_count": users_count,
                                                   "tickets_count": tickets_count,
                                                   "workshops_count": workshops_count,
                                                   "infographics_count": infographics_count,
                                                   "workshop_requests_count": workshop_requests_count,
                                                   "ambassadors_count": ambassadors_count,
                                                   "workshop_evaluations_count": workshop_evaluations_count})

@login_required
def profile(request):
    te_user = models.ThinkingEnvUser.objects.get(username = request.user)
    return render(request, 'tems/profile.html', {"user": te_user})

@login_required
def profile_edit(request):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    form = forms.ThinkingEnvironmentUserForm(instance=te_user)
    if request.method == "POST":
        form = forms.ThinkingEnvironmentUserForm(instance=te_user, data=request.POST)
        if form.is_valid:
            form.save()
            messages.success(request, "تم تحديث ملفكم بنجاح")
            return HttpResponseRedirect("/tems/profile")
    return render(request, 'tems/profile_edit.html', {"form": form,"user": te_user})

def profile_password(request):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    if request.method == "POST":
        current_password = request.POST["current_password"]
        new_password = request.POST["new_password"]
        repeat_password = request.POST["repeat_password"]
        user = authenticate(username=request.user, password=current_password)
        print(user)
        if user == None:
            messages.error(request, "كلمة المرور الحالية غير صحيحة")
            return HttpResponseRedirect("/tems/profile/password")
        else:
            if new_password != repeat_password:
                messages.error(request, "كلمات المرور غير متطابقة")
            else:
                user.set_password(new_password)
                user.save()
                login(request, user)
                messages.success(request, "تم تغيير كلمة المرور بنجاح")
                return HttpResponseRedirect("/tems/profile")
    return render(request,'tems/profile_password.html', {"user": te_user})

@login_required
def user_list(request):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    users = models.ThinkingEnvUser.objects.all()
    return render(request, 'tems/user_list.html', {"user":te_user, "users": users})

@login_required
def user_add(request):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    form = forms.ThinkingEnvironmentAddUserForm()
    if request.method == "POST":
        form = forms.ThinkingEnvironmentAddUserForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.created_manually = True
            new_user.save()
            messages.success(request, "تم اضافة مستخدم جديد بنجاح")
            return HttpResponseRedirect("/tems/users/")
    return render(request, 'tems/user_add.html', {"user": te_user, "form": form})

@login_required
def ticket_list(request):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    tickets = models.Ticket.objects.all()
    open_tickets = tickets.filter(status="open")
    closed_tickets = tickets.filter(status="closed")
    return render(request, 'tems/ticket_list.html', {"user":te_user,
                                                     "tickets": tickets,
                                                     "open_tickets": open_tickets,
                                                     "closed_tickets": closed_tickets})

@login_required
def ticket_detail(request, pk):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    ticket = get_object_or_404(models.Ticket, pk=pk)
    return render(request, "tems/ticket_detail.html", {"user": te_user, "ticket": ticket})

@login_required
def ticket_edit(request, pk):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    ticket = get_object_or_404(models.Ticket, pk=pk)
    status1 = ticket.status
    form = forms.TicketForm(instance=ticket)
    if request.method == "POST":
        form = forms.TicketForm(instance=ticket,data=request.POST)
        if form.is_valid():
            form.save()
            if form.cleaned_data['answer']:
                ticket.replier = request.user.id
                ticket.save()
                status2 = ticket.status
                if status1 == "open" and status2 == "closed":
                    notification_title = 'تم الرد على استشارتكم : "{}"'.format(ticket.title)
                    apns_device = APNSDevice.objects.filter(user=ticket.user)
                    if apns_device:
                        apns_device.send_message(notification_title)
                    gcm_device = GCMDevice.objects.filter(user=ticket.user)
                    if gcm_device:
                        gcm_device.send_message(notification_title)
            messages.success(request, "تم تعديل الاستشارة بنجاح")
            return HttpResponseRedirect("/tems/tickets/{}".format(ticket.pk))
    return render(request, "tems/ticket_edit.html", {"user": te_user,"ticket": ticket, "form": form})

@login_required
def workshop_list(request):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    workshops = models.Workshop.objects.all()
    return render(request, 'tems/workshop_list.html', {"user": te_user, "workshops": workshops})

@login_required
def workshop_detail(request, pk):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    workshop = get_object_or_404(models.Workshop, pk=pk)
    return render(request, "tems/workshop_detail.html", {"user": te_user, "workshop": workshop})

@login_required
def workshop_edit(request,pk):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    workshop = get_object_or_404(models.Workshop, pk=pk)
    form = forms.WorkshopForm(instance=workshop)
    if request.method == "POST":
        form = forms.WorkshopForm(request.POST, request.FILES, instance=workshop)
        if form.is_valid():
            form.save()
            messages.success(request, "تمت تعديل الدورة بنجاح")
            return HttpResponseRedirect("/tems/workshops/{}/".format(workshop.pk))
    return render(request, "tems/workshop_edit.html", {"user": te_user, "form": form, "workshop": workshop})

@login_required
def workshop_add(request):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    form = forms.WorkshopForm()
    if request.method == "POST":
        form = forms.WorkshopForm(request.POST, request.FILES)
        if form.is_valid():
            workshop = form.save()
            apns_devices = APNSDevice.objects.all()
            gcm_devices = GCMDevice.objects.all()
            notification_title = "دورة جديدة : {}".format(workshop.title)
            if apns_devices:
                apns_devices.send_message(notification_title)
            if gcm_devices:
                gcm_devices.send_message(notification_title)
            messages.success(request, "تمت اضافة دورة جديدة بنجاح")
            return HttpResponseRedirect("/tems/workshops/")
    return render(request, "tems/workshop_edit.html", {"user": te_user, "form": form})

@login_required
def workshop_delete(request,pk):
    workshop = get_object_or_404(models.Workshop, pk=pk)
    workshop.poster.delete(False)
    workshop.delete()
    messages.success(request, "تم حذف الدورة بنجاح")
    return HttpResponseRedirect("/tems/workshops/")

@login_required
def workshop_registration_delete(request,pk):
    workshop_registration = get_object_or_404(models.WorkshopRegistration, pk=pk)
    workshop = workshop_registration.workshop
    workshop_registration.delete()
    messages.success(request, "تم حذف الاشتراك بنجاح")
    return HttpResponseRedirect("/tems/workshops/{}/".format(workshop.pk))


@login_required
def workshop_requests_list(request):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    workshop_requests = models.WorkshopRequest.objects.all()
    return render(request, 'tems/workshop_requests_list.html', {"user": te_user, "workshop_requests": workshop_requests})

@login_required
def workshop_request_detail(request, pk):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    workshop_request = get_object_or_404(models.WorkshopRequest, pk=pk)
    return render(request, "tems/workshop_requests_detail.html", {"user": te_user, "workshop_request": workshop_request})

@login_required
def change_workshop_request_status(request, pk):
    workshop_request = get_object_or_404(models.WorkshopRequest, pk=pk)
    if workshop_request.status == "open":
        workshop_request.status = "closed"
    else:
        workshop_request.status = "open"
    workshop_request.save()
    return HttpResponseRedirect("/tems/workshop_requests/{}/".format(workshop_request.pk))

@login_required
def infographic_list(request):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    infographics = models.Infographic.objects.all()
    return render(request, 'tems/infographic_list.html', {"user": te_user, "infographics": infographics})

@login_required
def infographic_add(request):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    form = forms.InfographicForm()
    if request.method == "POST":
        #for file in request.FILES.getlist('image'):
        form = forms.InfographicForm(request.POST, request.FILES)
        if form.is_valid():
            for image in request.FILES.getlist('image'):
                models.Infographic.objects.create(image = image)
            messages.success(request, "تمت اضافة انفوجرافيك جديد بنجاح")
        return HttpResponseRedirect("/tems/infographics/")
    return render(request, "tems/infographic_add.html", {"user": te_user, "form": form})

@login_required
def infographic_delete(request,pk):
    infographic = get_object_or_404(models.Infographic, pk=pk)
    infographic.image.delete_thumbnails()
    infographic.image.delete(False)
    infographic.delete()
    messages.success(request, "تم حذف الانفوجرافيك بنجاح")
    return HttpResponseRedirect("/tems/infographics/")

@login_required
def ambassador_requests_list(request):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    ambassador_requests = models.AmbassadorRequest.objects.all()
    return render(request, "tems/ambassador_requests_list.html", {"user": te_user, "ambassador_requests": ambassador_requests})

@login_required
def ambassador_request_detail(request, pk):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    ambassador_request = get_object_or_404(models.AmbassadorRequest, pk=pk)
    return render(request, "tems/ambassador_requests_detail.html", {"user": te_user, "ambassador_request": ambassador_request})

@login_required
def change_ambassador_request_status(request, pk):
    ambassador_request = get_object_or_404(models.AmbassadorRequest, pk=pk)
    if ambassador_request.status == "open":
        ambassador_request.status = "closed"
    else:
        ambassador_request.status = "open"
    ambassador_request.save()
    return HttpResponseRedirect("/tems/ambassador_requests/{}/".format(ambassador_request.pk))

@login_required
def workshop_evaluations_list(request):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    workshop_evaluations = models.WorkshopEvaluation.objects.all()
    return render(request, "tems/workshop_evaluations_list.html", {"user": te_user, "workshop_evaluations": workshop_evaluations})

@login_required
def workshop_evaluation_detail(request, pk):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    workshop_evaluation = get_object_or_404(models.WorkshopEvaluation, pk=pk)
    return render(request, "tems/workshop_evaluations_detail.html", {"user": te_user, "workshop_evaluation": workshop_evaluation})

@login_required
def book_list(request):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    books = models.Book.objects.all()
    return render(request, "tems/book_list.html", {"user": te_user, "books": books})

@login_required
def book_add(request):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    form = forms.BookForm()
    if request.method == "POST":
        form = forms.BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "تمت اضافة كتيب جديد بنجاح")
            return HttpResponseRedirect("/tems/books/")
    return render(request, "tems/book_add.html", {"user": te_user, "form": form})

def book_edit(request,pk):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    book = get_object_or_404(models.Book, pk=pk)
    form = forms.BookForm(instance=book)
    if request.method == "POST":
        form = forms.BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "تمت تعديل الكتيب بنجاح")
            return HttpResponseRedirect("/tems/books/")
    return render(request, "tems/book_add.html", {"user": te_user, "form": form, "book": book})

def book_delete(request,pk):
    book = get_object_or_404(models.Book, pk=pk)
    book.file.delete(False)
    book.delete()
    messages.success(request, "تم حذف الكتيب بنجاح")
    return HttpResponseRedirect("/tems/books/")


@login_required
def ambassador_country_list(request):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    countries = models.AmbassadorCountry.objects.all()
    return render(request, "tems/ambassador_country_list.html", {"user": te_user, "countries": countries})

@login_required
def ambassador_country_add(request):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    form = forms.AmbassadorCountryForm()
    formset = forms.AmbassadorCityFormset(queryset = form.instance.ambassadorcity_set.all())
    if request.method == "POST":
        form = forms.AmbassadorCountryForm(request.POST)
        formset = forms.AmbassadorCityFormset(request.POST, queryset = form.instance.ambassadorcity_set.all())
        if form.is_valid() and formset.is_valid():
            country = form.save()
            cities = formset.save(commit=False)
            for city in cities:
                city.ambassador_country = country
                city.save()
            messages.success(request, "تمت اضافة دولة جديدة بنجاح")
            return HttpResponseRedirect("/tems/ambassador_countries/")
    return render(request, "tems/ambassador_country_add.html", {"user": te_user, "form": form, "formset": formset})

@login_required
def ambassador_country_edit(request,pk):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    country = get_object_or_404(models.AmbassadorCountry, pk=pk)
    form = forms.AmbassadorCountryForm(instance=country)
    formset = forms.AmbassadorCityFormset(queryset=form.instance.ambassadorcity_set.all())
    if request.method == "POST":
        form = forms.AmbassadorCountryForm(request.POST,instance=country)
        formset = forms.AmbassadorCityFormset(request.POST, queryset=form.instance.ambassadorcity_set.all())
        if form.is_valid() and formset.is_valid():
            form.save()
            cities = formset.save(commit=False)
            for city in cities:
                city.ambassador_country = country
                city.save()
            messages.success(request, "تمت تعديل الدولة بنجاح")
            return HttpResponseRedirect("/tems/ambassador_countries/{}/".format(country.pk))
    return render(request, "tems/ambassador_country_add.html", {"user": te_user, "form": form, "country": country, "formset":formset})

@login_required
def ambassador_country_delete(request,pk):
    country = get_object_or_404(models.AmbassadorCountry, pk=pk)
    country.delete()
    messages.success(request, "تم حذف الدولة بنجاح")
    return HttpResponseRedirect("/tems/ambassador_countries/")

@login_required
def ambassador_country_detail(request,pk):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    country = get_object_or_404(models.AmbassadorCountry, pk=pk)
    return render(request, "tems/ambassador_country_detail.html", {"user": te_user, "country": country})

@login_required
def ambassador_city_detail(request, country_pk, city_pk):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    country = get_object_or_404(models.AmbassadorCountry, pk=country_pk)
    city = get_object_or_404(models.AmbassadorCity, pk=city_pk)
    return render(request, "tems/ambassador_city_detail.html", {"user": te_user, "country": country, "city": city})

@login_required
def ambassador_city_edit(request, country_pk, city_pk):
    te_user = models.ThinkingEnvUser.objects.get(username=request.user)
    country = get_object_or_404(models.AmbassadorCountry, pk=country_pk)
    city = get_object_or_404(models.AmbassadorCity, pk=city_pk)
    form = forms.AmbassadorCityForm(instance=city)
    formset = forms.AmbassadorExtraRepresentativeFormset(queryset=form.instance.ambassadorextrarepresentative_set.all())
    if request.method == "POST":
        form = forms.AmbassadorCityForm(request.POST,instance=city)
        formset = forms.AmbassadorExtraRepresentativeFormset(
            request.POST, queryset=form.instance.ambassadorextrarepresentative_set.all())
        if form.is_valid() and formset.is_valid():
            form.save()
            reps = formset.save(commit=False)
            for rep in reps:
                rep.ambassador_city = city
                rep.save()
            for rep in formset.deleted_objects:
                rep.delete()
            messages.success(request, "تمت تعديل المدينة بنجاح")
            return HttpResponseRedirect("/tems/ambassador_countries/{}/city/{}/".format(country_pk, city_pk))
    return render(request, "tems/ambassador_city_edit.html", {"user": te_user, "country": country, "city": city, "form": form, "formset": formset})

@login_required
def ambassador_city_delete(request, country_pk, city_pk):
    country = get_object_or_404(models.AmbassadorCountry, pk=country_pk)
    city = get_object_or_404(models.AmbassadorCity, pk=city_pk)
    city.delete()
    messages.success(request, "تم حذف المدينة بنجاح")
    return HttpResponseRedirect("/tems/ambassador_countries/{}".format(country.pk))