from django.db import models


class Sellers(models.Model):
    name = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=300, null=True)
    password = models.CharField(max_length=10, null=True)




    contact = models.CharField(max_length=12,blank=True,null=True)
    emailid = models.EmailField(max_length=50)
    verified = models.BooleanField(default=False)


    def __str__(self):
        return self.name


#class fileupload(models.Model):
