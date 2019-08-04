from django.conf.urls import url

from . import views

app_name = 'store'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^getverified/$', views.getverified, name='getverified'),
    url(r'^notverified/$', views.notverified, name='notverified'),
    url(r'^verification/$', views.verification, name='verification'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^myprofile/$', views.myprofile, name='myprofile'),
    url(r'^searchres/$', views.searchres, name='searchres'),
    url(r'^ajaxsearch/$', views.ajaxsearch, name='ajaxsearch'),
    url(r'^products/(?P<product_name>[ \t\n\r\f\vA-Za-z]+)/$', views.products, name='products'),
    url(r'^addtocart/$', views.add_to_cart, name='addtocart'),
    url(r'^cart/$', views.view_cart, name='viewcart'),
    url(r'^delitem/$', views.del_item, name='delitem'),
    url(r'^updateitem/$', views.update_item, name='updateitem'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^delcart/$', views.delcart, name='delcart'),
]
