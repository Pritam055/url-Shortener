from django import forms 

from .models import BitURL
from .validators import validate_dot_com, validate_url

class BiturlForm(forms.Form):
    url = forms.CharField(
         label = '',
         validators= [validate_url, validate_dot_com],
         widget = forms.TextInput(attrs = {
                'class':'form-control',
                'placeholder':'Long URL Here...'
         })
        )
