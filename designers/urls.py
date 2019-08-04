from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name='designers'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'register/$', views.DesignerCreate.as_view(), name='register'),
    url(r'login/$', views.login, name='login'),
    url(r'dashboard/$', views.registeration, name='registeration'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'registerconf/$', views.regcon, name='regcon'),
    url(r'our_designers', views.designersview, name='ourDes'),
    url(r'change_password/$', views.change_password, name='password_change'),
    url(r'wrong_password/$', views.wrongPassword, name='wrongPassword'),
    url(r'create_blog/$', views.blog, name='blog'),
    url(r'view_blogs/$',views.blog_search,name='blogsearch'),
    url(r'^(?P<status>[0-9]+)/$',views.next,name='next'),
    url(r'^dp_change/$',views.edit_dp,name='edit_dp'),
    url(r'^address_change/$',views.edit_address,name='edit_address'),
    url(r'^about_change/$',views.edit_about,name='edit_about'),
    url(r'^jobs/$',views.myjobs,name='myjobs'),
    url(r'^editjob/$',views.editjob,name='editjob'),
    url(r'^update/$',views.update,name='update'),
    url(r'^requestitem',views.requestitem,name='requestitem'),
    #url(r'^design/$', views.designs, name='design'),
    url(r'^login1/$', views.login1, name='login1'),
    url(r'^logout1/$', views.logout1, name='logout1'),
    url(r'^edit_des/$',views.edit_designs,name='edit_designs'),
    url(r'^forgotpass/$', views.forgotpass, name='fp'),
    url(r'^forgotpass/update/$', views.passmatch, name='fpu'),
    url(r'^resendotp/$', views.resendotp, name='reotp'),
    url(r'^test/$', views.test, name='test'),



]
