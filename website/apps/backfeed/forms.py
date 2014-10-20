from django import forms
from backfeed.models import Backfeed

from settings import *




class BackfeedForm(forms.ModelForm):
    
    class Meta():
        model = Backfeed
        #exclude = ('creator', 'updated', 'created','topic', 'user_ip',)

    def clean_message(self):
        message = self.cleaned_data["message"]
        error = None
        if error:
            raise forms.ValidationError("Got error: %s" % error)
        
        return message
