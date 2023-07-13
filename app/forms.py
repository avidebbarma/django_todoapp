from .models import Todoapp
from django.forms import ModelForm


class taskform(ModelForm):
    class Meta:
        model=Todoapp
        fields=["title", "description", "complete" ]