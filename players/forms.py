from django.forms import ModelForm

from .models import Player, Note

class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ['ckey']


class NoteCreateForm(ModelForm):
    class Meta:
        model = Note
        fields = ['text']
