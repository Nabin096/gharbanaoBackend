from django import forms
from designers.models import Designers

class SendMails(forms.Form):
    Send_To = forms.CharField(max_length=30,null=True)


    def clean_message(self):
        Send_To=self.cleaned_data.get("Send_To")

        return Send_To
