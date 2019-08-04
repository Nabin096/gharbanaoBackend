from designers.models import *

import django_filters
from django import forms


class CustomerSearchFilter(django_filters.FilterSet):
    name=django_filters.CharFilter(lookup_expr='icontains')
    firmname = django_filters.CharFilter(lookup_expr='icontains')
    address = django_filters.CharFilter(lookup_expr='icontains',)
    Traditional=django_filters.BooleanFilter(widget=forms.CheckboxInput).field_class(initial=True)
    Modern = django_filters.BooleanFilter(widget=forms.CheckboxInput,).field_class(initial=True)
    Minimalistic = django_filters.BooleanFilter(widget=forms.CheckboxInput).field_class(initial=True)
    Contemporary = django_filters.BooleanFilter(widget=forms.CheckboxInput).field_class(initial=True)
    Industrial = django_filters.BooleanFilter(widget=forms.CheckboxInput).field_class(initial=True)
    MidCenturyModern = django_filters.BooleanFilter(widget=forms.CheckboxInput).field_class(initial=True)
    Scandinian = django_filters.BooleanFilter(widget=forms.CheckboxInput).field_class(initial=True)
    Bohemian = django_filters.BooleanFilter(widget=forms.CheckboxInput).field_class(initial=True)
    Retro = django_filters.BooleanFilter(widget=forms.CheckboxInput).field_class(initial=True)

    class Meta:
        model = Designers
        fields = ['name','firmname','address','Traditional','Modern','Minimalistic','Contemporary','Industrial','MidCenturyModern','Scandinian','Bohemian','Retro',]


class BlogSearchFilter(django_filters.Filter):
    searchfield=django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model= Blogs
        fields=['title','subject','author.name']