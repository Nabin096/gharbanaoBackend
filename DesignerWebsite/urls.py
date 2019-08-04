from django.conf import settings
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.contrib import admin
from django.core.mail import send_mail
from django.shortcuts import render
from designers.models import Designers,Rawpass

from designers.forms import SendMail
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import routers
from apis import views
from rest_framework.urlpatterns import format_suffix_patterns
import random
import string
from django.contrib.auth.hashers import make_password

from designers.models import Designers


def Mail(request):
    email=""
    if request.method == "POST":
        MyRegisterForm = SendMail(request.POST)
        if MyRegisterForm.is_valid():
            Send_To=MyRegisterForm.cleaned_data['Send_To']
            dbuser = Designers.objects.filter(email=Send_To)
            if dbuser:
                user=dbuser[0]
                randpass=''.join(random.choice(string.ascii_uppercase+string.digits) for _ in range(8))
                dbuser[0].password=make_password(randpass)
                dbuser[0].designerID='GBIDX0{0}'.format(Designers.objects.count())
                rawpass=Rawpass(rawpass=randpass,designer=dbuser[0])
                rawpass.save()
                dbuser[0].save()
                contact_message =  'your userId and password is {0} {1}'.format(user.designerID,randpass)
                from_email = settings.EMAIL_HOST_USER
                to_email = []
                to_email.append(Send_To)
                send_mail('Registration Succesfull', contact_message, from_email, to_email, fail_silently=False)



        else:
            MyRegisterForm = SendMail(request.GET)

    return render(request, 'designers/SendMails.html',{})



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^designers/',include('designers.urls')),
    url(r'^',include('customers.urls')),
    #url(r'^store/', include('store.urls')),
    url(r'^mail/',  admin.site.admin_view(Mail), name='Mail'),
    url(r'^andro/',include('apis.urls')),
    #url(r'^seller/',include('seller.urls')),
]

urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
