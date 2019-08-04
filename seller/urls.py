from django.conf.urls import url

from . import views

app_name = 'seller'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$',views.register,name='register'),
    url(r'^dashboard/$',views.dashboard,name='dashboard'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^add_product/$', views.add, name='add'),

]