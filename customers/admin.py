from django.contrib import admin
from  .models import Job,Complains,Updates


# Register your models here.
admin.site.register(Job)
admin.site.register(Complains)
admin.site.register(Updates)
