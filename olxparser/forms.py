from django import forms

from olxparser.models import Submarket
from olxparser.spyder import OlxSpyder
from .tasks import olx_stat_task, send_email_task, run_stat_task


class IndexForm(forms.Form):
    submarketurl = forms.URLField(widget=forms.URLInput)
    email = forms.EmailField(widget=forms.EmailInput)

    def clean_submarketurl(self):
        url = self.cleaned_data['submarketurl']
        if 'olx.ua' not in url:
            raise forms.ValidationError('Please enter url belongs to "https://www.olx.ua"')
        return url

    def save(self):
        data = self.cleaned_data
        submarket = Submarket.objects.create(**data)
        pk = submarket.pk
        url = data['submarketurl']
        #olx_stat_task.delay(pk, url)
        run_stat_task.delay(pk, url)
