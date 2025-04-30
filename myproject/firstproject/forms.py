from django import forms
from .models import Clothes


class ClothesForms(forms.ModelForm):
    
    class Meta:
        model = Clothes
        fields = ('name','description','price', 'color','photo','is_exists','category', 'collection')

