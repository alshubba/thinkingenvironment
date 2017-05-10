from django.contrib.admin.widgets import AdminDateWidget
from django.forms import ModelForm, Textarea, SelectDateWidget, PasswordInput
from django.utils.translation import ugettext_lazy as _

from . import models

class ThinkingEnvironmentUserForm(ModelForm):
    class Meta:
        model = models.ThinkingEnvUser
        fields = ['first_name','last_name','email','country','city','neighborhood','sex', 'marital_status']
        labels = {
            'first_name': _('الإسم الأول'),
            'last_name': _('اسم العائلة'),
            'email': _('البريد الإلكتروني'),
            'phone': _('رقم الجوال'),
            'country': _('الدولة'),
            'city': _('المدينة'),
            'neighborhood': _('الحي'),
            'sex': _('الجنس'),
            'marital_status': _('الحالة الإجتماعية')
        }

class ThinkingEnvironmentAddUserForm(ModelForm):
    class Meta:
        model = models.ThinkingEnvUser
        fields = ['username','password','first_name','last_name','email','role']
        labels = {
            'username': _('اسم المستخدم'),
            'password': _('كلمة المرور'),
            'first_name': _('الإسم الأول'),
            'last_name': _('اسم العائلة'),
            'email': _('البريد الإلكتروني'),
            'role': _('نوع المستخدم')
        }
        widgets = {
            'password': PasswordInput,
        }
        help_texts = {
            'username': '',
        }

class TicketForm(ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['answer','status','open_to_public' ]
        widgets = {
            'answer': Textarea(attrs={'cols': 80, 'rows': 20}),
        }
        labels = {
            'answer': _('الرد'),
            'status': _('الحالة'),
            'open_to_public': _('عام')
        }

class WorkshopForm(ModelForm):
    class Meta:
        model = models.Workshop
        fields = ['title', 'presenter', 'begin_date', 'end_date', 'price','poster']
        labels = {
            'title': _('العنوان'),
            'presenter': _('المدرب'),
            'begin_date': _('يوم البدء'),
            'end_date': _('يوم الانتهاء'),
            'price': _('السعر'),
            'poster': _('البوستر')
        }

        widgets = {
            'begin_date': SelectDateWidget,
            'end_date': SelectDateWidget
        }

class InfographicForm(ModelForm):
    class Meta:
        model = models.Infographic
        fields = ['image']
        labels = {
            'image': _('حمل الصورة')
        }

class BookForm(ModelForm):
    class Meta:
        model = models.Book
        fields = ['title', 'description', 'file']
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 20}),
        }
        labels = {
            'title': _('العنوان'),
            'description': _('الشرح'),
            'file': _('حمل الملف')
        }
