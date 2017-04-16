from django.contrib.admin.widgets import AdminDateWidget
from django.forms import ModelForm, Textarea, SelectDateWidget, ImageField
from django.utils.translation import ugettext_lazy as _

from . import models

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