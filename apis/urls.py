from django.conf.urls import url
from functools import wraps
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name='apis'


def csrf_exempt(view_func):
    def wrapped_view(request,*args,**kwargs):
        return view_func(request,*args,**kwargs)
    wrapped_view.csrf_exempt=True
    return wraps(view_func,)(wrapped_view)


urlpatterns = format_suffix_patterns( [
    url(r'^hu/$', views.IndexViewSet.as_view()),
    url(r'^humi/$', csrf_exempt(views.Login.as_view())),
    url(r'^humis/$', csrf_exempt(views.SearchBlogs.as_view())),
    url(r'^ru/$', csrf_exempt(views.CreateBlog.as_view())),
    url(r'^rumi/$', csrf_exempt(views.DesignerBlogs.as_view())),
    url(r'^rumis/$', csrf_exempt(views.LikeView.as_view())),
    url(r'^sayonara/$', csrf_exempt(views.Logout.as_view())),



    url(r'^sl/$', csrf_exempt(views.StoreLogin.as_view())),
])
