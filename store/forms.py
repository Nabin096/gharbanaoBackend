from django import forms

from designers.models import Designers


class StoreLoginForm(forms.Form):
    designerID = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput())


class VerificationForm(forms.Form):
    verificationImage = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(VerificationForm, self).__init__(*args, **kwargs)
        self.fields['verificationImage'].required = False


class SearchForm(forms.Form):
    select = forms.CharField()
    search = forms.CharField()


class AddressForm(forms.Form):
    name = forms.CharField()
    firmname = forms.CharField()
    number = forms.IntegerField
    email = forms.EmailField()
    city = forms.CharField()
    state = forms.CharField()
    address = forms.CharField()
    pincode = forms.IntegerField()
