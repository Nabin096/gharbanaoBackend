from django.db import models
from django.core.urlresolvers import reverse
from datetime import datetime,date



# Create your models here.
class Designers(models.Model):
    designerID = models.CharField(max_length=15,null=True,blank=True)
    name = models.CharField(max_length=25,null=True)
    firmname = models.CharField(max_length=30,null=True)
    contact = models.CharField(max_length=10,null=True)
    address = models.TextField(max_length=200,null=True)
    profilepic = models.ImageField(null=True,blank=True)
    email = models.EmailField(max_length=30,primary_key=True)
    password = models.CharField(max_length=1000,null=True)
    points = models.IntegerField(null=True,default=100)
    design1 = models.ImageField(null=True,blank=True)
    design2 = models.ImageField(null=True,blank=True)
    design3 = models.ImageField(null=True,blank=True)
    AboutMe = models.TextField(max_length=200,null=True,default="Please tell us about your personallity and why shoud customers be interested in you")
    AboutYourDesigns = models.TextField(max_length=200,null=True,default="Please tell us about your design styles")
    PortfolioFilled = models.BooleanField(default=False)
    Traditional = models.BooleanField(default=False)
    Modern = models.BooleanField(default=False)
    Minimalistic = models.BooleanField(default=False)
    Contemporary = models.BooleanField(default=False)
    Industrial = models.BooleanField(default=False)
    MidCenturyModern = models.BooleanField(default=False)
    Scandinian = models.BooleanField(default=False)
    Bohemian = models.BooleanField(default=False)
    Retro = models.BooleanField(default=False)
    status =models.IntegerField(default=1)






    def get_absolute_url(self):
        return reverse('designers:regcon')


    def __str__(self):
        return self.name

class DesignTypes(models.Model):
    designer = models.OneToOneField(Designers,on_delete=models.CASCADE)
    name = designer.name
    Traditional = models.BooleanField(default=False)
    Modern = models.BooleanField(default=False)
    Minimalistic = models.BooleanField(default=False)
    Contemporary = models.BooleanField(default=False)
    Industrial = models.BooleanField(default=False)
    MidCenturyModern = models.BooleanField(default=False)
    Scandinian = models.BooleanField(default=False)
    Bohemian = models.BooleanField(default=False)
    Retro = models.BooleanField(default=False)


    def __str__(self):
        return self.designer.__str__()


class Designs(models.Model):
    designer = models.OneToOneField(Designers,on_delete=models.CASCADE)
    points=models.IntegerField(blank=True,null=True)
    design1 = models.CharField(null=True,max_length=40)
    design2 = models.CharField(null=True,max_length=40)
    design3 = models.CharField(null=True,max_length=40)


    def __str__(self):
        return self.designer.__str__()

class BlogLiked(models.Model):
    likedBy=models.CharField(max_length=15)
    likedTo=models.ForeignKey(Designers,on_delete=models.CASCADE,null=True,blank=True)
    blogID=models.IntegerField(default=-1)

    def __str__(self):
        return self.likedTo.name


class Blogs(models.Model):
    author=models.ForeignKey(Designers,null=True,blank=True,on_delete=models.CASCADE)
    title=models.CharField(max_length=25)
    subject=models.CharField(max_length=1000)
    requestedBy=models.CharField(max_length=30,null=True,blank=True)
    views=models.IntegerField(default=0)
    likes=models.IntegerField(default=0)
    shares=models.IntegerField(default=0)
    image=models.ImageField(null=True,blank=True)
    dated = models.DateTimeField( default=datetime.now)
    comments=models.IntegerField(default=0)
    day=models.DateField(default=datetime.now())





    def __str__(self):
        return self.title


class Comments(models.Model):
    body=models.CharField(max_length=200)
    commenter=models.CharField(max_length=40)
    blogID = models.IntegerField(default=-1)
    commentedTo=models.ForeignKey(Designers,on_delete=models.CASCADE,null=True,blank=True)
    author=models.CharField(null=True,blank=True,max_length=25)


    def __str__(self):
        return self.body

class Rawpass(models.Model):
    designer=models.ForeignKey(Designers,on_delete=models.CASCADE)
    rawpass=models.CharField(max_length=1000,null=True,blank=True)

    def __str__(self):
        return self.designer.name


class RequestItem(models.Model):
    designer = models.ForeignKey(Designers, on_delete=models.CASCADE)
    object =  models.CharField(max_length=50)
    qty=models.IntegerField()
    price=models.IntegerField(null=True,blank=True)
    status=models.CharField(default='N/A',max_length=50)
    viewed=models.BooleanField(default=False)
    requirements=models.CharField(null=True,blank=True,max_length=100)

    def __str__(self):
        myname=repr(self.designer.name)+' '+repr(self.viewed)
        return myname

