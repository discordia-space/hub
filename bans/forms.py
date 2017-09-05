from django.forms import ModelForm
from .models import Ban


class BanForm(ModelForm):
    class Meta:
        model = Ban
        fields = ["description", "reasons", "expiration_time"]
