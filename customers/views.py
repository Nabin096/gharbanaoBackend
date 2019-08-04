from django.shortcuts import render
from django.http import HttpResponse
from designers.models import Designers,Blogs
from .filters import CustomerSearchFilter,BlogSearchFilter
from .forms import *
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from designers.models import *
from rest_framework import routers
from apis import views
from rest_framework.urlpatterns import format_suffix_patterns
import random
import string
from django.views.decorators.cache import cache_control
# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if  request.session.has_key('job'):

        del request.session['job']
    toppers=Designers.objects.order_by('-points')[:5]
    topper1=toppers[0]
    topper2 = toppers[1]
    topper3 = toppers[2]
    topper4 = toppers[3]
    topper5=toppers[4]

    content={
        'topper1':topper1,
        'topper2':topper2,
        'topper3':topper3,
        'topper4':topper4,
        'topper5':topper5
    }

    return render(request, 'customers/home.html', content)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def search(request):
    search_text=""
    designer=None
    designer_list=Designers.objects.all().order_by('-points')
    designer_filter=CustomerSearchFilter(request.GET, queryset=designer_list)
    if request.method == "POST":
        search_text = request.POST['search_text']
        if(search_text==""):
            designer=None
        else:
            designer = Designers.objects.filter(name__contains=search_text)

    if  request.session.has_key('job'):
        search_text = ""
        designer = None
        designer_list = Designers.objects.filter(PortfolioFilled=True).order_by('-points')
        designer_filter = CustomerSearchFilter(request.GET, queryset=designer_list)
        if request.method == "POST":
            search_text = request.POST['search_text']
            if (search_text == ""):
                designer = None
            else:
                designer = Designers.objects.filter(name__contains=search_text)

            return render(request, 'customers/ajax_search.html', {'designers': designer})
        return render(request, 'customers/search.html', {'filter': designer_filter, 'designers': designer})
    if  request.session.has_key('job'):

        del request.session['job']
    toppers=Designers.objects.order_by('-points')[:5]
    topper1=toppers[0]
    topper2 = toppers[1]
    topper3 = toppers[2]
    topper4 = toppers[3]
    topper5=toppers[4]

    content={
        'topper1':topper1,
        'topper2':topper2,
        'topper3':topper3,
        'topper4':topper4,
        'topper5':topper5
    }
    return render(request, 'customers/home.html',content )





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def blogs(request):
    if  request.session.has_key('job'):

        del request.session['job']
    searchfield=""
    searchentry=BlogsForm(request.GET)
    blogList=Blogs.objects.filter().order_by('-day')
    if searchentry.is_valid():
        blogList = []
        searchfield=list(set(searchentry.cleaned_data['searchfield'].split(sep=" ")))
        for x in searchfield:
            newBlogs = Blogs.objects.filter(title__contains=x)
            print(len(newBlogs))
            if len(newBlogs)<3and len(newBlogs)>0:
                blogList.extend(newBlogs)
                blogList = list(set(blogList))
            newBlogs1 = Blogs.objects.filter(subject__contains=x)
            if len(newBlogs1)<3 and len(newBlogs1)>0:
                blogList.extend(newBlogs1)
                blogList = list(set(blogList))

    content={'blogList':blogList}




    return render(request,'customers/blogs.html',content)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def job(request):
    try :
        print(request.session['job'])
    except:
        pass
    if request.method=="POST":

        jobinitial=JobInitial(request.POST)
        print(jobinitial.errors)
        if jobinitial.is_valid():
            resultset=[]
            roomtype = jobinitial.cleaned_data['roomtype']
            resultset.append(roomtype)
            lifespan = jobinitial.cleaned_data['lifespan']
            resultset.append(lifespan)
            choice = jobinitial.cleaned_data['execution']

            if choice=="Yes":
                execution=True
            else:
                execution=False
            resultset.append(execution)
            area = jobinitial.cleaned_data['area']
            resultset.append(area)
            estimatedbudget =jobinitial.cleaned_data['estimatedbudget']
            resultset.append(estimatedbudget)

            reqr=[]
            #requirements=requirements+jobinitial.cleaned_data['false_ceiling']
            if jobinitial.cleaned_data['false_ceiling']=='on':
                reqr.append('False Ceiling')
            if jobinitial.cleaned_data['flooring']=='on':
                reqr.append('Flooring')
            if jobinitial.cleaned_data['wall_paper']=='on':
                reqr.append('Wall Paper')
            if jobinitial.cleaned_data['wall_painting']=='on':
                reqr.append('Wall painting')
            if jobinitial.cleaned_data['luxury_goods']=='on':
                reqr.append('Luxury Goods')
            requirements = ",".join(reqr)
            #print(requirements)
            resultset.append(requirements)
            request.session['job'] = resultset
            print("{0}".format(request.session['job']))
            designer_list = Designers.objects.filter(PortfolioFilled=True).order_by('-points')
            designer_filter = CustomerSearchFilter(request.GET, queryset=designer_list)
            return render(request, 'customers/search.html', {'filter': designer_filter})
    if  request.session.has_key('job'):

        del request.session['job']
    toppers=Designers.objects.order_by('-points')[:5]
    topper1=toppers[0]
    topper2 = toppers[1]
    topper3 = toppers[2]
    topper4 = toppers[3]
    topper5=toppers[4]

    content={
        'topper1':topper1,
        'topper2':topper2,
        'topper3':topper3,
        'topper4':topper4,
        'topper5':topper5
    }

    return render(request,'customers/home.html',content)


def job2(request):

    if request.method=="POST":


        jobsecond=JobSecondStage(request.POST)
        print(jobsecond.errors)
        if jobsecond.is_valid():
            resultset=request.session['job']
            email = request.POST['email']
            resultset.append(email)
            freetime = request.POST['freetime']
            contact=request.POST['contact']
            resultset.append(freetime)
            name=request.POST['name']
            resultset.append(name)
            resultset.append(contact)
            request.session['job']=resultset
            print(request.session['job'])
            contact_message = 'your userId and password is {0}'.format(resultset[7])
            from_email = settings.EMAIL_HOST_USER
            to_email = []
            to_email.append(resultset[8])
            send_mail('Registration Succesfull', contact_message, from_email, to_email, fail_silently=False)

            return render(request,'customers/otp.html',{})
    return render(request,'customers/job2.html',{})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def designer(request):
    if request.session.has_key('job'):
        designer = None
        if request.method == "POST":
            designer = Designers.objects.filter(designerID=request.POST['designer'])
            print(designer)
            blogList = Blogs.objects.filter(author=Designers.objects.filter(designerID=request.POST['designer'])).order_by('-dated')
            return render(request, 'customers/designerselect.html', {'designer': designer,'blogList': blogList})
        return render(request, 'customers/designerselect.html', {'designer': designer})
    if  request.session.has_key('job'):

        del request.session['job']
    toppers=Designers.objects.order_by('-points')[:5]
    topper1=toppers[0]
    topper2 = toppers[1]
    topper3 = toppers[2]
    topper4 = toppers[3]
    topper5=toppers[4]

    content={
        'topper1':topper1,
        'topper2':topper2,
        'topper3':topper3,
        'topper4':topper4,
        'topper5':topper5
    }
    return render(request, 'customers/home.html', content)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def designer_selected(request):
    email=""
    if request.session.has_key('job'):
        if request.method=="POST":
            resultset=request.session['job']
            designer=request.POST['designerselected']
            resultset.append(designer)
            randpass = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
            print(randpass)
            resultset.append(randpass)
            request.session['job']=resultset
            print(request.session['job'])


            return render(request, 'customers/job2.html', {})
        else:
            return render(request, 'customers/job2.html', {})
    if  request.session.has_key('job'):

        del request.session['job']
    toppers=Designers.objects.order_by('-points')[:5]
    topper1=toppers[0]
    topper2 = toppers[1]
    topper3 = toppers[2]
    topper4 = toppers[3]
    topper5=toppers[4]

    content={
        'topper1':topper1,
        'topper2':topper2,
        'topper3':topper3,
        'topper4':topper4,
        'topper5':topper5
    }
    return render(request, 'customers/home.html',content)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def otp(request):
    if request.session.has_key('job'):
        if request.method=="POST":
            otp = Otp(request.POST)
            print(otp.errors)
            if otp.is_valid():
                resultset = request.session['job']
                otppass=otp.cleaned_data['otp']
                print(otppass)
                if resultset[7]==otppass:
                    print('hurrah')

                print("{0}".format(request.session['job']))

                #return render(request, 'customers/make_payment.html', {})
                print(request.session['job'])
                resultset = request.session['job']
                randpass = ''.join(random.choice(string.digits) for _ in range(4))
                print(randpass)
                contact_message = 'your userId and password is {0}'.format(randpass)
                from_email = settings.EMAIL_HOST_USER
                to_email = []
                to_email.append(request.session['job'][8])
                send_mail('Registration Succesfull', contact_message, from_email, to_email, fail_silently=False)
                job = Job()
                job.roomtype = resultset[0]
                job.lifespan = resultset[1]
                job.execution = resultset[2]
                job.area = resultset[3]
                job.estimatedbudget = resultset[4]
                if not resultset[5] == '':
                    job.requirements = resultset[5]

                job.email = resultset[8]
                job.date = resultset[9]
                job.name = resultset[10]
                job.contact=resultset[11]

                #name not saving
                job.designer = Designers.objects.filter(designerID=resultset[6])[0]
                job.designer.points += 100
                job.designer.save()
                print(resultset[6])

                job.password = randpass
                job.save()
                print(Job.objects.get(email=resultset[8]))
                del request.session['job']
        else:
            return render(request, 'customers/otp.html', {})
    if  request.session.has_key('job'):

        del request.session['job']
    toppers=Designers.objects.order_by('-points')[:5]
    topper1=toppers[0]
    topper2 = toppers[1]
    topper3 = toppers[2]
    topper4 = toppers[3]
    topper5=toppers[4]

    content={
        'topper1':topper1,
        'topper2':topper2,
        'topper3':topper3,
        'topper4':topper4,
        'topper5':topper5
    }
    return render(request,'customers/home.html',content)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def make_payment(request):
    if request.session.has_key('job'):
     return render(request,'customers/make_payment.html',{})
    return render(request, 'customers/home.html', {})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def successfull(request):
    if request.session.has_key('job'):
        print(request.session['job'])
        resultset=request.session['job']
        randpass = ''.join(random.choice(string.digits) for _ in range(4))
        print(randpass)
        contact_message = 'your userId and password is {0}'.format(randpass)
        from_email = settings.EMAIL_HOST_USER
        to_email = []
        to_email.append(request.session['job'][8])
        send_mail('Registration Succesfull', contact_message, from_email, to_email, fail_silently=False)
        job=Job()
        job.roomtype = resultset[0]
        job.lifespan = resultset[1]
        job.execution = resultset[2]
        job.area = resultset[3]
        job.estimatedbudget = resultset[4]
        if not resultset[5]=='':
            job.requirements = resultset[6]

        job.email = resultset[8]
        job.date=resultset[9]
        job.name=resultset[10]
        job.designer=Designers.objects.filter(designerID=resultset[6])[0]
        job.designer.points+=100
        job.designer.save()
        print(resultset[6])

        job.password = randpass
        job.save()
        print(Job.objects.get(email=resultset[8]))
        del request.session['job']
        return render(request, 'customers/successfull.html', {})
    if  request.session.has_key('job'):

        del request.session['job']
    toppers=Designers.objects.order_by('-points')[:5]
    topper1=toppers[0]
    topper2 = toppers[1]
    topper3 = toppers[2]
    topper4 = toppers[3]
    topper5=toppers[4]

    content={
        'topper1':topper1,
        'topper2':topper2,
        'topper3':topper3,
        'topper4':topper4,
        'topper5':topper5
    }
    return render(request, 'customers/home.html', content)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.session.has_key('customer'):
        j=Job.objects.filter(id=request.session['customer'])
        c = Complains.objects.filter(by=Job.objects.filter(id=request.session['customer'])[0]).order_by('-date')
        u = Updates.objects.filter(job=Job.objects.filter(id=request.session['customer'])[0]).order_by('-date')
        print(Job.objects.filter(id=request.session['customer'])[0])
        d = Job.objects.filter(id=request.session['customer'])[0].designer
        content = {
            'complains': c,
            'job': j[0],
            'u': u,
            'd':d
        }
        return render(request, 'customers/job_detail.html', content)

    if request.method == "GET":
        if request.session.has_key('job'):
            del request.session['job']
        toppers = Designers.objects.order_by('-points')[:5]
        topper1 = toppers[0]
        topper2 = toppers[1]
        topper3 = toppers[2]
        topper4 = toppers[3]
        topper5 = toppers[4]

        content = {
                'topper1': topper1,
                'topper2': topper2,
                'topper3': topper3,
                'topper4': topper4,
                'topper5': topper5}

        return render(request, 'customers/home.html', content)
    if request.method=="POST":
        log = LoginForm(request.POST)
        print(log.errors)
        if log.is_valid():
            email = log.cleaned_data['email']
            password = log.cleaned_data['password']
            x= Job.objects.filter(email=email,password=password)
            if x:
                if x[0].job_started:
                    request.session['customer']=x[0].id
                    print(x[0])
                    c = Complains.objects.filter(by=x[0])
                    u = Updates.objects.filter(job=Job.objects.filter(id=request.session['customer'])[0]).order_by('-date')
                    d = Job.objects.filter(id=request.session['customer'])[0].designer
                    print(u)
                    content = {
                        'complains': c,
                        'job': x[0],
                        'd':d,
                        'u': u
                    }
                    return render(request, 'customers/job_detail.html', content)

                else :
                    return render(request,'customers/wait.html',{})
        else:
             print('not user')
             return render(request,'customers/login_error.html')

        if request.session.has_key('job'):
                del request.session['job']
        toppers = Designers.objects.order_by('-points')[:5]
        topper1 = toppers[0]
        topper2 = toppers[1]
        topper3 = toppers[2]
        topper4 = toppers[3]
        topper5 = toppers[4]

        content = {
                    'topper1': topper1,
                    'topper2': topper2,
                    'topper3': topper3,
                    'topper4': topper4,
                    'topper5': topper5
                }
        return render(request, 'customers/home.html',content)




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    try:
        del request.session['customer']
    except:
        pass
    if  request.session.has_key('job'):

        del request.session['job']
    toppers=Designers.objects.order_by('-points')[:5]
    topper1=toppers[0]
    topper2 = toppers[1]
    topper3 = toppers[2]
    topper4 = toppers[3]
    topper5=toppers[4]

    content={
        'topper1':topper1,
        'topper2':topper2,
        'topper3':topper3,
        'topper4':topper4,
        'topper5':topper5
    }
    return render(request,'customers/home.html', content)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile_handler(request):
    if request.session.has_key('customer'):
        complains = ComplainForm(request.GET)
        print(complains.errors)
        if complains.is_valid():
            complain=complains.cleaned_data['complain']
            com=Complains()
            com.complain=complain
            com.to=Job.objects.filter(id=request.session['customer'])[0].designer
            com.to.points=com.to.points-20
            com.by=Job.objects.filter(id=request.session['customer'])[0]
            com.save()
            com.to.save()
            j = Job.objects.filter(id=request.session['customer'])
            c=Complains.objects.filter(by=j[0])
            u = Updates.objects.filter(job=Job.objects.filter(id=request.session['customer'])[0]).order_by('-date')
            d=Job.objects.filter(id=request.session['customer'])[0].designer
            print(j[0])
            content={
                'complains':c,
                'job': j[0],
                'u': u,
                'd':d
            }
            return render(request, 'customers/job_detail.html', content)
    if  request.session.has_key('job'):

        del request.session['job']
    toppers=Designers.objects.order_by('-points')[:5]
    topper1=toppers[0]
    topper2 = toppers[1]
    topper3 = toppers[2]
    topper4 = toppers[3]
    topper5=toppers[4]

    content={
        'topper1':topper1,
        'topper2':topper2,
        'topper3':topper3,
        'topper4':topper4,
        'topper5':topper5
    }
    return render(request,'customers/home.html', content)







@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update(request):
    if request.session.has_key('customer'):
        if request.method=='POST':
            updateform=Updatesform(request.POST,request.FILES)
            if updateform.is_valid():
                myupdate=Updates()
                myupdate.article=updateform.cleaned_data['article']
                myupdate.image=updateform.cleaned_data['image']
                myupdate.author=Job.objects.filter(id=request.session['customer'])[0].name
                myupdate.date=datetime.now()
                myupdate.job=Job.objects.filter(id=request.session['customer'])[0]
                myupdate.save()
        j = Job.objects.filter(id=request.session['customer'])
        c = Complains.objects.filter(by=j[0])
        u = Updates.objects.filter(job=Job.objects.filter(id=request.session['customer'])[0]).order_by('-date')
        d = Job.objects.filter(id=request.session['customer'])[0].designer


        content = {
            'complains': c,
            'job': j[0],
            'u':u,
            'd':d

        }
        return render(request, 'customers/job_detail.html', content)
    if  request.session.has_key('job'):

        del request.session['job']
    toppers=Designers.objects.order_by('-points')[:5]
    topper1=toppers[0]
    topper2 = toppers[1]
    topper3 = toppers[2]
    topper4 = toppers[3]
    topper5=toppers[4]
    content = {
        'topper1': topper1,
        'topper2': topper2,
        'topper3': topper3,
        'topper4': topper4,
        'topper5': topper5
    }
    return render(request, 'customers/home.html', content)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def howitworks(request):
    return render(request,'customers/howitworks.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ourdesign(request):
    form = DesignSearch(request.GET)
    desi = Designers.objects.filter(PortfolioFilled=True).order_by('-points')[:15]

    ourimg = []
    for x in desi:
        obj = []
        obj.append(x.design1.url)
        obj.append(x)
        ourimg.append(obj)

    search_field = 'Featured'
    if form.is_valid():
        ourimg = []
        search_field = form.cleaned_data['search']
        Designers1 = list(Designs.objects.filter(design1=search_field).order_by('-points')[:5])
        Designers2 = list(Designs.objects.filter(design2=search_field).order_by('-points')[:5])
        Designers3 = list(Designs.objects.filter(design3=search_field).order_by('-points')[:5])


        try:
            for x in Designers1:

                obj=[]
                obj.append(x.designer.design1.url)
                obj.append(x.designer)
                ourimg.append(obj)

        except:
            pass
        try:
            for x in Designers2:
                obj = []
                obj.append(x.designer.design2.url)
                obj.append(x.designer)
                ourimg.append(obj)


        except:
            pass
        try:

            for x in Designers3:
                obj = []
                obj.append(x.designer.design3.url)
                obj.append(x.designer)
                ourimg.append(obj)


        except:
            pass

        content = {

            'header': search_field,
            'ourimg':ourimg
        }
        for x in ourimg:
            print(x)
        return render(request, 'customers/designs.html', content)
    content = {

        'header': search_field,
        'ourimg':ourimg

    }

    return render(request, 'customers/designs.html', content)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def testblogs(request):
    return render(request,'customers/testblogs.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def resend(request):
    if request.session.has_key('job'):
        if request.method=="POST":
            randpass = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
            print(randpass)
            request.session['job'][7]=randpass
            a=[]

            a.append(request.session['job'][8])
            contact_message = 'your userId and password is {0}'.format(randpass)
            print(contact_message)
            from_email = settings.EMAIL_HOST_USER
            send_mail('Registration Succesfull', contact_message, from_email, a, fail_silently=False)

            return render(request, 'customers/otp.html', {})


def specific_blog(request):
    if request.method=='GET':
        myform=SelectBlog(request.GET)
        if myform.is_valid():
            id=myform.cleaned_data['url']
            myblog=Blogs.objects.filter(id=id)[0]
            print(myblog)
            content={
                'b':myblog
            }
            return  render(request,'customers/blog_select.html',content)

def test(request):
    return render(request, 'customers/test.html', {})
