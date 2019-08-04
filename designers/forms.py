from django import forms

from .models import Designers

class DesignerDetails(forms.Form):
    designerID = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_message(self):
        print("Hello")
        designerID=self.cleaned_data.get("designerID")
        password=self.cleaned_data("password")
        dbuser=Designers.objects.filter(designerID=designerID)
        if not dbuser:
            raise forms.ValidationError("User does not exist in our db!")
        return designerID

class SendMail(forms.Form):
    Send_To=forms.CharField(max_length=30)


class PortfolioDetails(forms.Form):
    AboutMe = forms.CharField(max_length=200)
    AboutYourDesigns = forms.CharField(max_length=300)
    design2 = forms.ImageField()
    design3 = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(PortfolioDetails, self).__init__(*args, **kwargs)
        self.fields['design2'].required = False
        self.fields['design3'].required=False

    def clean_message(self):
        cleaned_data=super(PortfolioDetails, self).clean()
        AboutMe=cleaned_data.get("AboutMe")
        AboutYourDesigns=cleaned_data.get("AboutYourDesigns")
        design2=cleaned_data.get("design2")
        design3=cleaned_data.get("design3")
        return AboutMe


class ConfirmPasswordForm(forms.Form):
    old_password=forms.CharField(widget=forms.PasswordInput())
    new_password=forms.CharField(widget=forms.PasswordInput())
    def clean_message(self):
        cleaned_data=super(ConfirmPasswordForm, self).clean()
        old_password=cleaned_data.get("old_password")
        new_password=cleaned_data.get("new_password")
        return old_password


class BlogForm(forms.Form):
    title=forms.CharField()
    content=forms.CharField()
    image=forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False



class Comment(forms.Form):
    matter=forms.CharField()
    id=forms.IntegerField()





class DpForm(forms.Form):
    profilepic = forms.ImageField()

    def save(self,id):
        user=Designers.objects.filter(designerID=id)
        user[0].profilepic=self.cleaned_data['profilepic']
        user[0].save(update_fields=['profilepic'])








class DesignsForm(forms.Form):
    design1 = forms.ImageField()
    design1type = forms.CharField()
    design2 = forms.ImageField()
    design2type = forms.CharField()
    design3 = forms.ImageField()
    design3type = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(DesignsForm, self).__init__(*args, **kwargs)
        self.fields['design1'].required = False
        self.fields['design2'].required = False
        self.fields['design3'].required=False

class AboutForm(forms.Form):
    AboutMe = forms.CharField()
    AboutYourDesigns = forms.CharField()


class AddressForm(forms.Form):
    address=forms.CharField()



class AboutEditForm(forms.Form):
    AboutMe = forms.CharField(required=False)
    AboutYourDesigns = forms.CharField(required=False)

class DesignsEditForm(forms.Form):
    design1 = forms.ImageField(required=False)
    design1type = forms.CharField(required=False)
    design2 = forms.ImageField(required=False)
    design2type = forms.CharField(required=False)
    design3 = forms.ImageField(required=False)
    design3type = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(DesignsEditForm, self).__init__(*args, **kwargs)
        self.fields['design1'].required = False
        self.fields['design2'].required = False
        self.fields['design3'].required = False



class jobselect(forms.Form):
    jobid=forms.CharField()


class UpdatesJobform(forms.Form):
    id=forms.CharField()
    image = forms.ImageField(required=False)
    article = forms.CharField(max_length=500)


class RequestForm(forms.Form):
    object = forms.CharField()
    qty = forms.IntegerField()
    requirements = forms.CharField(required=False)

class Forgotpass(forms.Form):
    email=forms.CharField()


class fppass(forms.Form):
    otp=forms.CharField()
    password=forms.CharField()


class Loginform(forms.Form):
    userid=forms.CharField()
    password=forms.CharField()

class Designeditform(forms.Form):
    selected=forms.CharField()
    design=forms.ImageField()
    designtype=forms.CharField()

