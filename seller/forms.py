from django import forms


class SellerDetails(forms.Form):
    name = forms.CharField(max_length=15)
    emailid = forms.EmailField(max_length=50)
    contact = forms.CharField(max_length=12)
    address = forms.CharField()
    password = forms.CharField(max_length=1000)


class LoginCheck(forms.Form):
    emailid = forms.EmailField(max_length=50)
    password = forms.CharField(max_length=1000)


class ProductEntryForm(forms.Form):
    name = forms.CharField()
    company = forms.CharField()
    price = forms.DecimalField()
    availability = forms.CharField()
    category = forms.CharField()
    other = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(ProductEntryForm, self).__init__(*args, **kwargs)
        self.fields['other'].required = False


class ProductSearchForm(forms.Form):
    searchfield=forms.CharField()