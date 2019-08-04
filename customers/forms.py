from django import forms

class BlogsForm(forms.Form):
    searchfield=forms.CharField()

class JobInitial(forms.Form):
    roomtype=forms.CharField()
    lifespan=forms.CharField()
    execution=forms.CharField()
    area=forms.FloatField()
    estimatedbudget=forms.IntegerField()
    #requirements=forms.CharField(required=False)
    false_ceiling=forms.CharField(required=False)
    flooring=forms.CharField(required=False)
    wall_paper=forms.CharField(required=False)
    wall_painting=forms.CharField(required=False)
    luxury_goods=forms.CharField(required=False)




class JobSecondStage(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    freetime=forms.DateTimeInput()
    contact=forms.CharField()

class Otp(forms.Form):
    otp=forms.CharField()


class LoginForm(forms.Form):
    email=forms.EmailField()
    password=forms.CharField()



class ComplainForm(forms.Form):
    complain=forms.CharField()
    time=forms.DateInput()


class DesignSearch(forms.Form):
    search=forms.CharField()


class Updatesform(forms.Form):
    image = forms.ImageField(required=False)
    article = forms.CharField(max_length=500)


class SelectBlog(forms.Form):
    url=forms.IntegerField()