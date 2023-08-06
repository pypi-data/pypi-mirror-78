from django import forms
from django.utils.translation import gettext_lazy as _
from .form import Form
from .widgets import TextInput, Textarea


class ContactForm(Form):
    subject = forms.CharField(
        max_length=60,
        widget=TextInput,
        label=_('Subject')
    )
    content = forms.CharField(
        widget=Textarea,
        label=_('Message')
    )

    def send_message(self):
        pass
