from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name='customers'


urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^designs$', views.search,name='search'),
    url(r'^blogs$',views.blogs,name='blogs'),
    url(r'^job_description$',views.job,name='job'),
    url(r'^job_personal$',views.job2,name='job2'),
    url(r'^designer_select$',views.designer,name='designer'),
    url(r'^designer_selected$',views.designer_selected,name='designer_selected'),
    url(r'^otp', views.otp, name='otp'),
    url(r'^make_payment$', views.make_payment, name='make_payment'),
    url(r'^successfull$',views.successfull, name='successfull'),
    url(r'^login$',views.login, name='login'),
    url(r'^logout$',views.logout, name='logout'),
    url(r'^profile_details',views.profile_handler,name='profile_handler'),
    url(r'^update_post',views.update,name="update"),
    url(r'^howitworks',views.howitworks,name='howitworks'),
    url(r'^ourdesign$',views.ourdesign,name='ourdesign'),
    #url(r'^testing$',views.testblogs,name='testblogs'),
    url(r'^blogview/$', views.specific_blog, name='specific_blog'),
    url(r'^resend$', views.resend, name='resend'),
    url(r'^test$', views.test, name='test'),










]