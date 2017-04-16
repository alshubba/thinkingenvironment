from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from push_notifications.models import APNSDevice, GCMDevice

from . import models
from . import forms



from django.core.signals import request_finished
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from . import serializers

"""

@receiver(request_finished)
def my_callback(sender, **kwargs):
    print("Request finished!")

"""

@receiver(post_save, sender = models.Ticket)
def post_save_callback(sender, instance, **kwargs):
    serializer = serializers.models.Ticket(instance)
    print(instance)
    print(serializer.data)


def forgot_password(request,token):
    user = get_object_or_404(models.ThinkingEnvUser, forgot_password_token = token)
    return render(request, "tems/forgot_password.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            teUser = models.ThinkingEnvUser.objects.get(username=user.username)
            if (teUser.role == "admin") or (teUser.role == "expert") or (teUser.role == "user"):
                login(request, user)
                return HttpResponseRedirect("/tems/dashboard")
            else:
                messages.error(request, "عذرا  ولكن  هذه  الصفحة  مخصصة  فقط  للمدراء  والخبراء")
        else:
            messages.error(request, "اسم  المستخدم  أو  كلمة  المرور  غير  صحيح")
    return render(request, 'tems/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/tems/login")

@login_required
def dashboard(request):
    users_count = models.ThinkingEnvUser.objects.count()
    tickets_count = models.Ticket.objects.filter(status="open").count()
    workshops_count = models.Workshop.objects.count()
    infographics_count = models.Infographic.objects.count()
    workshop_requests_count = models.WorkshopRequest.objects.filter(status="open").count()
    ambassadors_count = models.AmbassadorRequest.objects.filter(status="open").count()
    workshop_evaluations_count = models.WorkshopEvaluation.objects.count()
    return render(request, 'tems/dashboard.html', {"users_count": users_count,
                                                   "tickets_count": tickets_count,
                                                   "workshops_count": workshops_count,
                                                   "infographics_count": infographics_count,
                                                   "workshop_requests_count": workshop_requests_count,
                                                   "ambassadors_count": ambassadors_count,
                                                   "workshop_evaluations_count": workshop_evaluations_count})

@login_required
def ticket_list(request):
    tickets = models.Ticket.objects.all()
    open_tickets = tickets.filter(status="open")
    closed_tickets = tickets.filter(status="closed")
    return render(request, 'tems/ticket_list.html', {"tickets": tickets,
                                                     "open_tickets": open_tickets,
                                                     "closed_tickets": closed_tickets})

@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(models.Ticket, pk=pk)
    return render(request, "tems/ticket_detail.html", {"ticket": ticket})

@login_required
def ticket_edit(request, pk):
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
                    device = APNSDevice.objects.filter(user=ticket.user)
                    print(device)
                    device.send_message("تم الرد على استشارتكم '{}'".format(ticket.title))
            messages.success(request, "تم تعديل الاستشارة بنجاح")
            return HttpResponseRedirect("/tems/tickets/{}".format(ticket.pk))
    return render(request, "tems/ticket_edit.html", {"ticket": ticket, "form": form})

@login_required
def workshop_list(request):
    workshops = models.Workshop.objects.all()
    return render(request, 'tems/workshop_list.html', {"workshops": workshops})

@login_required
def workshop_detail(request, pk):
    workshop = get_object_or_404(models.Workshop, pk=pk)
    return render(request, "tems/workshop_detail.html", {"workshop": workshop})

@login_required
def workshop_edit(request,pk):
    workshop = get_object_or_404(models.Workshop, pk=pk)
    form = forms.WorkshopForm(instance=workshop)
    if request.method == "POST":
        form = forms.WorkshopForm(request.POST, request.FILES, instance=workshop)
        if form.is_valid():
            form.save()
            messages.success(request, "تمت تعديل الدورة بنجاح")
            return HttpResponseRedirect("/tems/workshops/{}/".format(workshop.pk))
    return render(request, "tems/workshop_edit.html", {"form": form, "workshop": workshop})

@login_required
def workshop_add(request):
    form = forms.WorkshopForm()
    if request.method == "POST":
        form = forms.WorkshopForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "تمت اضافة دورة جديدة بنجاح")
            return HttpResponseRedirect("/tems/workshops/")
    return render(request, "tems/workshop_edit.html", {"form": form})

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
    workshop_requests = models.WorkshopRequest.objects.all()
    return render(request, 'tems/workshop_requests_list.html', {"workshop_requests": workshop_requests})

@login_required
def workshop_request_detail(request, pk):
    workshop_request = get_object_or_404(models.WorkshopRequest, pk=pk)
    return render(request, "tems/workshop_requests_detail.html", {"workshop_request": workshop_request})

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
    infographics = models.Infographic.objects.all()
    return render(request, 'tems/infographic_list.html', {"infographics": infographics})

@login_required
def infographic_add(request):
    form = forms.InfographicForm()
    if request.method == "POST":
        form = forms.InfographicForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "تمت اضافة انفوجرافيك جديد بنجاح")
            return HttpResponseRedirect("/tems/infographics/")
    return render(request, "tems/infographic_add.html", {"form": form})

@login_required
def infographic_delete(request,pk):
    infographic = get_object_or_404(models.Infographic, pk=pk)
    infographic.image.delete(False)
    infographic.delete()
    messages.success(request, "تم حذف الانفوجرافيك بنجاح")
    return HttpResponseRedirect("/tems/infographics/")

@login_required
def ambassador_requests_list(request):
    ambassador_requests = models.AmbassadorRequest.objects.all()
    return render(request, "tems/ambassador_requests_list.html", {"ambassador_requests": ambassador_requests})

@login_required
def ambassador_request_detail(request, pk):
    ambassador_request = get_object_or_404(models.AmbassadorRequest, pk=pk)
    return render(request, "tems/ambassador_requests_detail.html", {"ambassador_request": ambassador_request})

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
    workshop_evaluations = models.WorkshopEvaluation.objects.all()
    return render(request, "tems/workshop_evaluations_list.html", {"workshop_evaluations": workshop_evaluations})

@login_required
def workshop_evaluation_detail(request, pk):
    workshop_evaluation = get_object_or_404(models.WorkshopEvaluation, pk=pk)
    return render(request, "tems/workshop_evaluations_detail.html", {"workshop_evaluation": workshop_evaluation})
















