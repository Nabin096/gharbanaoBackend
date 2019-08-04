from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail
from django.conf import settings
from . models import Designers,Blogs,BlogLiked,Comments,Designs,Rawpass
from . forms import *
from django.contrib.auth.hashers import make_password,check_password
from django.views.generic.edit import CreateView
from customers.models import *
from . forms import DesignerDetails, ConfirmPasswordForm, BlogForm, Comment, DpForm, AboutForm, DesignsForm
from . models import Designers, Blogs, BlogLiked, Comments, Designs, Rawpass
import random
import string

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if request.session.has_key('designerID'):
        try:
            del request.session['selectedjob']
        except:
            pass
        designerID = request.session['designerID']
        dbuser = Designers.objects.filter(designerID=designerID)
        blogList = Blogs.objects.filter(author=Designers.objects.filter(designerID=request.session['designerID'])[0].email).order_by('-dated')
        if dbuser[0].PortfolioFilled:
            context = {
                'dbuser': dbuser,
                'blogList':blogList
            }

            return render(request, 'designers/loggedin.html', context)
        elif dbuser:
            del request.session['designerID']
    context={

    }
    return render(request,'designers/index.html',context=context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def registeration(request):

    designerID=""
    password=""
    if request.method == "POST":
        if request.session.has_key('designerID'):
            try:
                del request.session['selectedjob']
            except:
                pass
            designerID = request.session['designerID']
            dbuser = Designers.objects.filter(designerID=designerID)
            blogList = Blogs.objects.filter(author=Designers.objects.filter(designerID=request.session['designerID'])[0].email).order_by('-dated')
            if dbuser and dbuser[0].PortfolioFilled==True:
                context = {
                    'dbuser': dbuser,
                    'blogList': blogList
                }
                return render(request, 'designers/loggedin.html', context)
        # Get the posted form
        MyRegisterForm = DesignerDetails(request.POST)
        form_errors= MyRegisterForm.errors
        content={
            'form':MyRegisterForm,
            'errors':  form_errors
        }
        print( MyRegisterForm.errors)
        if MyRegisterForm.is_valid():
            designerID=MyRegisterForm.cleaned_data['designerID']

            password=MyRegisterForm.cleaned_data['password']

            print(designerID)
            dbuser = Designers.objects.filter(designerID=designerID)
            if dbuser and check_password(password,dbuser[0].password):
                user = dbuser[0]
                #profilepic = user.profilepic.url
                request.session['designerID'] = designerID
                blogList = Blogs.objects.filter( author=Designers.objects.filter(designerID=request.session['designerID'])[0].email).order_by( '-dated')
                context = {
                    'dbuser': dbuser,
                    'blogList': blogList
                }
                if dbuser[0].PortfolioFilled == False:
                    context1 = {
                        'status': dbuser[0].status
                    }
                    return render(request, 'designers/dashboard.html', context1)
                return render(request, 'designers/loggedin.html', context)
            elif dbuser:
                return render(request, 'designers/register.html', {})
            if not dbuser:
                print("Not user")
                return render(request, 'designers/register.html', {})

        else:
            print("not valid")
            return render(request, 'designers/register.html', {})
    else:
        MyRegisterForm=DesignerDetails(request.GET)
        if request.session.has_key('designerID'):
            try:
                del request.session['selectedjob']
            except:
                pass
            designerID = request.session['designerID']
            dbuser = Designers.objects.filter(designerID=designerID)
            blogList = Blogs.objects.filter(author=Designers.objects.filter(designerID=request.session['designerID'])[0].email).order_by('-dated')
            context = {
                'dbuser': dbuser,
                'blogList': blogList
            }
            if dbuser[0].PortfolioFilled:
                return render(request, 'designers/loggedin.html', context)
            if dbuser[0].PortfolioFilled == False:
                context1 = {
                    'status': dbuser[0].status
                }
                return render(request, 'designers/dashboard.html', context1)


        return render(request, 'designers/register.html', {})

class DesignerCreate(CreateView):
    model=Designers
    fields = ['name','firmname','contact','email','address']


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    try:
        del request.session['designerID']
    except:
        pass
    return render(request, 'designers/logout.html', {})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.session.has_key('designerID'):
        try:
            del request.session['selectedjob']
        except:
            pass
        designerID = request.session['designerID']
        dbuser = Designers.objects.filter(designerID=designerID)
        if dbuser and dbuser[0].PortfolioFilled:
            user = dbuser[0]
            profilepic = user.profilepic.url
            blogList = Blogs.objects.filter(author=Designers.objects.filter(designerID=request.session['designerID'])[0].email).order_by('-dated')
            context = {
                'dbuser': dbuser,
                'blogList': blogList
            }
            return render(request, 'designers/loggedin.html', context)
        if dbuser and dbuser[0].PortfolioFilled == False:
            context1 = {
                'status': dbuser[0].status
            }
            return render(request, 'designers/dashboard.html', context1)

    return render(request, 'designers/register.html', {})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def regcon(request):
    if request.session.has_key('designerID'):
        try:
            del request.session['selectedjob']
        except:
            pass
        designerID = request.session['designerID']
        dbuser = Designers.objects.filter(designerID=designerID)
        if dbuser[0].PortfolioFilled:
            blogList = Blogs.objects.filter( author=Designers.objects.filter(designerID=request.session['designerID'])[0].email).order_by('-dated')
            context = {
                'dbuser': dbuser,
                'blogList': blogList
            }
            return render(request, 'designers/loggedin.html', context)
    context={

    }
    return render(request,'designers/regconfirm.html',context=context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def designersview(request):
    all_designers=Designers.objects.filter(PortfolioFilled=True).order_by('-points')
    context = {'all_designers':all_designers}
    return render(request, 'designers/our_designers.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def change_password(request):
    if not request.session.has_key('designerID'):
        return render(request, 'designers/register.html', {})
    old_password=""
    new_password=""
    if request.session.has_key('designerID') and request.method == "POST":
        try:
            del request.session['selectedjob']
        except:
            pass
        MyForm=ConfirmPasswordForm(request.POST)
        print(MyForm.errors)
        if MyForm.is_valid():
            old_password=MyForm.cleaned_data['old_password']
            new_password = MyForm.cleaned_data['new_password']
            if request.session.has_key('designerID'):
                designerID = request.session['designerID']
                user = Designers.objects.get(designerID=designerID)
                if user and check_password(old_password,user.password):
                    user.password = make_password(new_password)
                    rawp = Rawpass.objects.filter(designer=user)
                    rawp[0].rawpass = MyForm.cleaned_data['new_password']
                    rawp[0].save(update_fields=['rawpass'],force_update=True)
                    print(rawp[0].rawpass)
                    if user.status == 4:
                        user.status = 5
                        user.PortfolioFilled = True
                        user.save(update_fields=['password', 'status', 'PortfolioFilled'])
                        return render(request, 'designers/succesfull.html', {})
                    else:
                        user.save(update_fields=['password'])
                    dbuser = Designers.objects.filter(designerID=designerID)
                    blogList = Blogs.objects.filter(author=Designers.objects.filter(designerID=request.session['designerID'])[0].email).order_by('-dated')
                    if dbuser[0].PortfolioFilled:
                        context = {
                            'dbuser': dbuser,
                            'blogList': blogList
                        }
                        return render(request, 'designers/loggedin.html', context)
                else:
                    print('not user ')
                    del request.session['designerID']
                    return render(request, 'designers/WrongPassword.html', {})
            elif request.session.has_key('designerID') and request.method == "GET":
                return render(request, 'designers/changePassword.html', {})

            return render(request, 'designers/index.html', {})
    elif request.session.has_key('designerID') and request.method == "GET":
        try:
            del request.session['selectedjob']
        except:
            pass
        return render(request, 'designers/changePassword.html', {})

    return render(request, 'designers/index.html', {})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def wrongPassword(request):
    if not request.session.has_key('designerID'):
        try:
            del request.session['selectedjob']
        except:
            pass
        return render(request, 'designers/register.html', {})
    return render(request, 'designers/WrongPassword.html', {})


@cache_control(no_cache=True)
def blog(request):

    if request.session.has_key('designerID'):
        try:
            del request.session['selectedjob']
        except:
            pass
        title = ""
        content = ""
        image = None
        blogList=Blogs.objects.filter(author=Designers.objects.filter(designerID=request.session['designerID'])[0].email).order_by('-dated')
        con={
            'blogList':blogList
        }
        if request.method == "GET":
            dbuser = Designers.objects.filter(designerID=request.session['designerID'])
            context = {
                'dbuser': dbuser,
                'blogList': blogList
            }
            return render(request, 'designers/loggedin.html', context)
        if request.method == "POST":

            blog= BlogForm(request.POST)
            print(blog.errors)
            if blog.is_valid():
                title = blog.cleaned_data['title']
                content = blog.cleaned_data['content']
                try:
                 image = request.FILES['image']
                except:
                    pass
                new_blog=Blogs()
                new_blog.title=title
                new_blog.subject=content
                new_blog.image=image
                author=Designers.objects.filter(designerID=request.session['designerID'])[0]
                new_blog.author=author
                author.points=author.points+5
                new_blog.save()
                author.save(update_fields=['points'])
                dbuser=Designers.objects.filter(designerID=request.session['designerID'])
                context = {
                    'dbuser': dbuser,
                    'blogList': blogList
                }
                return render(request, 'designers/loggedin.html', context)


        else:
            blog=BlogForm(request.GET)
            print("hello")
        return render(request,'designers/blog.html',con)

    else:
        return render(request,'designers/register.html',{})


@cache_control(no_cache=True)
def blog_search(request):

    if request.session.has_key('designerID'):
        try:
            del request.session['selectedjob']
        except:
            pass
        blogList=Blogs.objects.filter().order_by('-day','-likes','-shares')
        likes = BlogLiked.objects.filter(likedBy=request.session['designerID'])

        com=Comment(request.GET)


        if com.is_valid():
            matter=com.cleaned_data['matter']
            id=com.cleaned_data['id']
            blogs = Blogs.objects.filter(id=id)
            comment=Comments(body=matter,commenter=request.session['designerID'],blogID=id,commentedTo=blogs[0].author,author=Designers.objects.filter(designerID=request.session['designerID'])[0].name)
            comment.save()
            myblog = Blogs.objects.filter(id=blogs[0].id)[0]
            myblog.comments = myblog.comments + 1
            myblog.save(update_fields=['comments'])


        likedBlogs = []

        for x in likes:
            likedBlogs.append(x.blogID)




        if request.method == "POST":

            blog=Blogs.objects.filter(id=request.POST['values'])
            likecheck=BlogLiked.objects.filter(likedBy=request.session['designerID'],likedTo=blog[0].author,blogID=blog[0].id)

            if not likecheck:
                like = BlogLiked(likedBy=request.session['designerID'], likedTo=blog[0].author,blogID=blog[0].id)
                like.save()
                likedBlogs.append(like.blogID)
                myblog=Blogs.objects.filter(id=blog[0].id)[0]
                myblog.likes = myblog.likes + 1

                myblog.save(update_fields=['likes'])
                print(Blogs.objects.filter(id=blog[0].id)[0].likes)
                myblog.author.points+=1
                print(myblog.author.points)

                myblog.author.save(update_fields=['points'])

        commentList={}
        for f in blogList:
            commentList[f] =Comments.objects.filter(blogID=f.id)


        content = {
            'blogList': blogList,
            'likedBlogs': likedBlogs,
            'commentList':commentList

        }
        return render(request,'designers/blogsearch.html',content)
    else :
        return render(request,'designers/register.html',{})





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def next(request, status):
    if request.method == "POST":

        profilepic = None
        design1 = None
        design1type = ""

        design2 = None
        design2type = ""
        design3 = None
        design3type = ""
        AboutMe = ""
        AboutYourDesigns = ""

        if request.session.has_key('designerID'):
            try:
                del request.session['selectedjob']
            except:
                pass

            designerID = request.session['designerID']

            dbuser = Designers.objects.filter(designerID=designerID)
            if dbuser:

                context = {
                    'dbuser': dbuser
                }
                if dbuser[0].status == 1:
                    print(request.FILES)
                    profilepic = request.FILES['profilepic']
                    print(request.FILES['profilepic'])
                    dbuser[0].profilepic = profilepic
                    dbuser[0].save(update_fields=['profilepic'], force_update=True)
                    dbuser[0].status += 1
                    dbuser[0].save()
                    context2 = {
                        'status': dbuser[0].status
                    }

                    return render(request, 'designers/' + str(dbuser[0].status) + '.html', context2)
                if dbuser[0].status == 2:
                    MyForm = DesignsForm(request.POST)
                    if MyForm.is_valid():
                        design1 = request.FILES['design1']
                        design1type = MyForm.cleaned_data['design1type']
                        design2 = request.FILES['design2']
                        design2type = MyForm.cleaned_data['design2type']
                        design3 = request.FILES['design3']
                        design3type = MyForm.cleaned_data['design3type']

                        dbuser[0].design1 = design1
                        dbuser[0].design2 = design2
                        dbuser[0].design3 = design3
                        dbuser[0].save(update_fields=['design1','design2','design3'], force_update=True)
                        dbuser[0].status += 1
                        dbuser[0].save()
                        if design1type=="Traditional" or design2type=="Traditional" or design3type=="Traditional":
                            dbuser[0].Traditional=True
                            dbuser[0].save(update_fields=['Traditional'])

                        if design1type=="Modern" or design2type=="Modern" or design3type=="Modern":
                            dbuser[0].Modern=True
                            dbuser[0].save(update_fields=['Modern'])

                        if design1type=="Minimalistic" or design2type=="Minimalistic" or design3type=="Minimalistic":
                            dbuser[0].Minimalistic=True
                            dbuser[0].save(update_fields=['Minimalistic'])

                        if design1type=="Contemporary" or design2type=="Contemporary" or design3type=="Contemporary":
                            dbuser[0].Contemporary=True
                            dbuser[0].save(update_fields=['Contemporary'])

                        if design1type=="Industrial" or design2type=="Industrial" or design3type=="Industrial":
                            dbuser[0].Industrial=True
                            dbuser[0].save(update_fields=['Industrial'])

                        if design1type=="MidCenturyModern" or design2type=="MidCenturyModern" or design3type=="MidCenturyModern":
                            dbuser[0].Traditional=True
                            dbuser[0].save(update_fields=['MidCenturyModern'])

                        if design1type=="Scandinian" or design2type=="Scandinian" or design3type=="Scandinian":
                            dbuser[0].Scandinian=True
                            dbuser[0].save(update_fields=['Scandinian'])

                        if design1type=="Bohemian" or design2type=="Bohemian" or design3type=="Bohemian":
                            dbuser[0].Bohemian=True
                            dbuser[0].save(update_fields=['Bohemian'])

                        if design1type=="Retro" or design2type=="Retro" or design3type=="Retro":
                            dbuser[0].Retro=True
                            dbuser[0].save(update_fields=['Retro'])

                        designtypo=Designs(design1=design1type,design2=design2type,design3=design3type,designer=dbuser[0],points=dbuser[0].points)
                        designtypo.save()
                        context2 = {
                            'status': dbuser[0].status
                        }

                        return render(request, 'designers/' + str(dbuser[0].status) + '.html', context2)
                if dbuser[0].status == 3:
                    MyForm = AboutForm(request.POST)
                    if MyForm.is_valid():
                        AboutMe = MyForm.cleaned_data['AboutMe']
                        AboutYourDesigns = MyForm.cleaned_data['AboutYourDesigns']
                        dbuser[0].AboutMe = AboutMe
                        dbuser[0].AboutYourDesigns = AboutYourDesigns
                        dbuser[0].save(update_fields=['AboutMe', 'AboutYourDesigns'], force_update=True)
                        dbuser[0].status += 1
                        dbuser[0].save()
                        context2 = {
                            'status': dbuser[0].status
                        }

                        return render(request, 'designers/changePassword.html', {})
                if dbuser[0].status == 4:
                    return render(request, 'designers/changePassword.html', {})



    else:
        if request.method == "GET":
            if request.session.has_key('designerID'):
                try:
                    del request.session['selectedjob']
                except:
                    pass
                designerID = request.session['designerID']

                dbuser = Designers.objects.filter(designerID=designerID)
                if dbuser:
                    context = {
                        'status': dbuser[0].status
                    }
                    if dbuser[0].status == 1:
                        MyForm = DpForm(request.GET)
                        return render(request, 'designers/' + str(dbuser[0].status) + '.html', context)
                    if dbuser[0].status == 2:
                        MyForm = DesignsForm(request.GET)
                        return render(request, 'designers/' + str(dbuser[0].status) + '.html', context)
                    if dbuser[0].status == 3:
                        MyForm = AboutForm(request.GET)
                        return render(request,'designers/'+ str(dbuser[0].status) +'.html',context)
                    if dbuser[0].status == 4:
                        return render(request, 'designers/changePassword.html', {})
                    return render(request,'designers/1.html',context)
            else:
                return render(request, 'designers/register.html', {})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_designs(request):
    if request.session.has_key('designerID'):
        des = Designers.objects.filter(designerID=request.session['designerID'])
        if request.method == 'POST':
            myform = Designeditform(request.POST, request.FILES)
            if myform.is_valid():

                desp = DesignTypes.objects.filter(designer=des[0])
                despt = Designs.objects.filter(designer=des[0])
                if myform.cleaned_data['selected'] == 'design1':
                    des.update(design1=myform.cleaned_data['design'])
                if myform.cleaned_data['selected'] == 'design2':
                    des.update(design2=myform.cleaned_data['design'])
                if myform.cleaned_data['selected'] == 'design3':
                    des.update(design3=myform.cleaned_data['design'])

                if myform.cleaned_data['selected'] == 'design1':
                    if myform.cleaned_data['designtype'] == 'Traditional':

                        desp.update(Traditional=True)
                        despt.update(design1='Traditional')

                    elif myform.cleaned_data['designtype'] == 'Modern':
                        desp.update(Modern=True)
                        despt.update(design1='Modern')
                    elif myform.cleaned_data['designtype'] == 'Minimalistic':
                        desp.update(Minimalistic=True)
                        despt.update(design1='Minimalistic')
                    elif myform.cleaned_data['designtype'] == 'Contemporary':
                        desp.update(Contemporary=True)
                        despt.update(design1='Contemporary')
                    elif myform.cleaned_data['designtype'] == 'MidCenturyModern':
                        desp.update(MidCenturyModern=True)
                        despt.update(design1='MidCenturyModern')
                    elif myform.cleaned_data['designtype'] == 'Scandidian':
                        desp.update(Scandidian=True)
                        despt.update(design1='Scandidian')

                    elif myform.cleaned_data['designtype'] == 'Bohemian':
                        desp.update(Bohemian=True)
                        despt.update(design1='Bohemian')

                    elif myform.cleaned_data['designtype'] == 'Retro':
                        desp.update(Retro=True)
                        despt.update(design1='Retro')

                if myform.cleaned_data['selected'] == 'design2':
                    if myform.cleaned_data['designtype'] == 'Traditional':

                        desp.update(Traditional=True)
                        despt.update(design2='Traditional')

                    elif myform.cleaned_data['designtype'] == 'Modern':
                        desp.update(Modern=True)
                        despt.update(design2='Modern')
                    elif myform.cleaned_data['designtype'] == 'Minimalistic':
                        desp.update(Minimalistic=True)
                        despt.update(design2='Minimalistic')
                    elif myform.cleaned_data['designtype'] == 'Contemporary':
                        desp.update(Contemporary=True)
                        despt.update(design2='Contemporary')
                    elif myform.cleaned_data['designtype'] == 'MidCenturyModern':
                        desp.update(MidCenturyModern=True)
                        despt.update(design2='MidCenturyModern')
                    elif myform.cleaned_data['designtype'] == 'Scandidian':
                        desp.update(Scandidian=True)
                        despt.update(design2='Scandidian')

                    elif myform.cleaned_data['designtype'] == 'Bohemian':
                        desp.update(Bohemian=True)
                        despt.update(design2='Bohemian')

                    elif myform.cleaned_data['designtype'] == 'Retro':
                        desp.update(Retro=True)
                        despt.update(design2='Retro')

                if myform.cleaned_data['selected'] == 'design3':
                    if myform.cleaned_data['designtype'] == 'Traditional':

                        desp.update(Traditional=True)
                        despt.update(design3='Traditional')

                    elif myform.cleaned_data['designtype'] == 'Modern':
                        desp.update(Modern=True)
                        despt.update(design3='Modern')
                    elif myform.cleaned_data['designtype'] == 'Minimalistic':
                        desp.update(Minimalistic=True)
                        despt.update(design3='Minimalistic')
                    elif myform.cleaned_data['designtype'] == 'Contemporary':
                        desp.update(Contemporary=True)
                        despt.update(design3='Contemporary')
                    elif myform.cleaned_data['designtype'] == 'MidCenturyModern':
                        desp.update(MidCenturyModern=True)
                        despt.update(design3='MidCenturyModern')
                    elif myform.cleaned_data['designtype'] == 'Scandidian':
                        desp.update(Scandidian=True)
                        despt.update(design3='Scandidian')

                    elif myform.cleaned_data['designtype'] == 'Bohemian':
                        desp.update(Bohemian=True)
                        despt.update(design3='Bohemian')

                    elif myform.cleaned_data['designtype'] == 'Retro':
                        desp.update(Retro=True)
                        despt.update(design3='Retro')
                blogList = Blogs.objects.filter(
                    author=Designers.objects.filter(designerID=request.session['designerID'])[0].email).order_by(
                    '-dated')
                context = {
                    'dbuser': des,
                    'blogList': blogList
                }
                return render(request, 'designers/loggedin.html', context)

            print(repr(myform.cleaned_data['selected']) + repr(myform.cleaned_data['designtype']) + repr(
                myform.cleaned_data['design']))
        blogList = Blogs.objects.filter(
            author=Designers.objects.filter(designerID=request.session['designerID'])[0].email).order_by(
            '-dated')
        context = {
            'dbuser': des,
            'blogList': blogList
        }
        return render(request, 'designers/loggedin.html', context)

    return render(request, 'designers/register.html', {})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_dp(request):
    if request.session.has_key('designerID'):
        try:
            del request.session['selectedjob']
        except:
            pass
        dbuser = Designers.objects.filter(designerID=request.session['designerID'])
        profilepic = None

        if request.method == "POST":
            form=DpForm(request.POST,request.FILES)
            print(form.errors)
            if form.is_valid():
                profilepic = request.FILES['profilepic']
                print(form.cleaned_data['profilepic'])
                form.save(request.session['designerID'])
                dbuser.update(profilepic=profilepic)
                dbuser[0].profilepic = form.cleaned_data['profilepic']
                dbuser[0].__dict__.update(profilepic=profilepic)
                dbuser[0].save(update_fields=['profilepic'], force_update=True)

                blogList = Blogs.objects.filter( author=Designers.objects.filter(designerID=request.session['designerID'])[0].email).order_by('-dated')

            context = {
                'dbuser': dbuser,
                'blogList': blogList
            }
            return render(request, 'designers/loggedin.html', context)
        blogList = Blogs.objects.filter(author=Designers.objects.filter(designerID=request.session['designerID'])[0].email).order_by('-dated')
        context = {
            'dbuser': dbuser,
            'blogList': blogList
        }
        return render(request, 'designers/loggedin.html', context)

    else:
        return render(request, 'designers/register.html', {})





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_address(request):
    if request.session.has_key('designerID'):
        try:
            del request.session['selectedjob']
        except:
            pass
        dbuser = Designers.objects.filter(designerID=request.session['designerID'])
        if request.method == "POST":
            form=AddressForm(request.POST)
            if form.is_valid():
                address=form.cleaned_data['address']
                dbuser.update(address=address)
                dbuser[0].save()
                blogList = Blogs.objects.filter( author=Designers.objects.filter(designerID=request.session['designerID'])[0].email).order_by('-dated')
                context = {
                    'dbuser': dbuser,
                    'blogList': blogList
                }
                return render(request, 'designers/loggedin.html', context)
        return render(request,'designers/addressupdate.html')
    else:
        return render(request, 'designers/register.html', {})




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_about(request):
    if request.session.has_key('designerID'):
        try:
            del request.session['selectedjob']
        except:
            pass
        dbuser = Designers.objects.filter(designerID=request.session['designerID'])
        if request.method == "POST":
            form = AboutEditForm(request.POST)

            if form.is_valid():
                AboutMe = form.cleaned_data['AboutMe']
                if not AboutMe =='':
                  dbuser.update(AboutMe=AboutMe)
                AboutYourDesigns=form.cleaned_data['AboutYourDesigns']
                if not AboutYourDesigns =='':
                    dbuser.update(AboutYourDesigns=AboutYourDesigns)

                dbuser[0].save()
                blogList = Blogs.objects.filter(author=Designers.objects.filter(designerID=request.session['designerID'])[0].email).order_by( '-dated')
                context = {
                    'dbuser': dbuser,
                    'blogList': blogList
                }

                return render(request, 'designers/loggedin.html', context)
        return render(request, 'designers/aboutform.html')
    else:
       return render(request, 'designers/register.html', {})






@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def myjobs(request):
    try:
        del request.session['selectedjob']
    except:
        pass
    if request.session.has_key('designerID'):
       jobs=Job.objects.filter(designer=Designers.objects.filter(designerID=request.session['designerID'])[0])
       context={
           'jobs':jobs
       }

       return render(request, 'designers/myjobs.html',context)

    return render(request, 'designers/register.html', {})

@cache_control(no_cache=True)
def editjob(request):
    if request.session.has_key('designerID'):
        if request.session.has_key('selectedjob'):
            job = Job.objects.filter(id=request.session['selectedjob'])[0]
            u = Updates.objects.filter(job=Job.objects.filter(id=request.session['selectedjob'])[0]).order_by('-date')[
                :10]
            context = {
                'j': job,
                'u': u
            }
            return render(request, 'designers/editjobs.html', context)

        jobs = Job.objects.filter(designer=Designers.objects.filter(designerID=request.session['designerID'])[0])
        context = {
            'jobs': jobs
        }
        if request.method=='POST':
            myform=jobselect(request.POST)
            if myform.is_valid():
                job=Job.objects.filter(id=myform.cleaned_data['jobid'])[0]
                request.session['selectedjob']=job.id
                u = Updates.objects.filter(job=Job.objects.filter(id=request.session['selectedjob'])[0]).order_by('-date')[:10]
                context = {
                    'j': job,
                    'u': u
                }
                return render(request,'designers/editjobs.html',context)

        return render(request, 'designers/myjobs.html', context)
    else:
        return render(request, 'designers/register.html', {})

@cache_control(no_cache=True)
def update(request):
    if request.session.has_key('designerID'):
        if request.method=='POST':
            updateform=UpdatesJobform(request.POST,request.FILES)
            if updateform.is_valid():
                myupdate=Updates()
                myupdate.article=updateform.cleaned_data['article']
                myupdate.image=updateform.cleaned_data['image']
                myupdate.author=Designers.objects.filter(designerID=request.session['designerID'])[0].name
                myupdate.date=datetime.now()
                myupdate.designer=True
                myupdate.job=Job.objects.filter(id=updateform.cleaned_data['id'])[0]
                myupdate.save()
                job = Job.objects.filter(id=updateform.cleaned_data['id'])[0]
                u = Updates.objects.filter(job=Job.objects.filter(id=request.session['selectedjob'])[0]).order_by('-date')[:10]
                context = {
                    'j': job,
                    'u' : u
                }
                return render(request, 'designers/editjobs.html', context)
        if request.session.has_key('selectedjob'):
            job = Job.objects.filter(id=request.session['selectedjob'])[0]
            u = Updates.objects.filter(job=Job.objects.filter(id=request.session['selectedjob'])[0]).order_by('-date')[
                :10]
            context = {
                'j': job,
                'u': u
            }
            return render(request, 'designers/editjobs.html', context)
        else:
            jobs = Job.objects.filter(designer=Designers.objects.filter(designerID=request.session['designerID'])[0])
            context = {
                'jobs': jobs
            }

            return render(request, 'designers/myjobs.html', context)
    return render(request, 'designers/register.html', {})




def requestitem(request):
    if request.session.has_key('designerID'):
        if request.method == 'POST':
            myform=RequestForm(request.POST)
            if myform.is_valid():
                myrequest=RequestItem()
                myrequest.object=myform.cleaned_data['object']
                myrequest.qty = myform.cleaned_data['qty']
                if myform.cleaned_data['requirements']:
                    myrequest.requirements=myform.cleaned_data['requirements']
                myrequest.designer=Designers.objects.get(designerID=request.session['designerID'])
                myrequest.save()


        requests=RequestItem.objects.filter(designer=Designers.objects.get(designerID=request.session['designerID']))
        content={
            'requests':requests
        }
        return render(request,'designers/requestitem.html',content)
    return render(request, 'designers/register.html', {})

















def login1(request):


    if request.session.has_key("user"):
        user = Designers.objects.filter(designerID=request.session['user'])
        if user:
            request.session['user'] = user[0].designerID


            context = {
                'user':user,

            }
            return render(request, 'gharbanao/designs.html', context)





    error=""
    if request.method=="POST":

        l=Loginform(request.POST)

        if l.is_valid():
            user=Designers.objects.filter(designerID=l.cleaned_data['userid'],password=l.cleaned_data['password'])
            if user:
                request.session['user']=user[0].designerID


                return render(request,'gharbanao/designs.html',{'user':user,})
            else:
                error="No user found"
    return render(request, 'gharbanao/login.html', {'e': error,})



def logout1(request):
    try:
        del request.session['user']
    except:
        pass
    error=""
    return render(request,'gharbanao/login.html',{'e':error})



def forgotpass(request):
    if request.method=="POST":

        mf=Forgotpass(request.POST)
        if mf.is_valid():

          fpp=Designers.objects.filter(email=mf.cleaned_data['email'])
          if fpp:
              randpass=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
              print(randpass)
              mail=[]
              mail.append(mf.cleaned_data['email'])
              #send mail giving OTP
              from_email = settings.EMAIL_HOST_USER
              send_mail('OTP','Your One Time Password is  Here:' + randpass, from_email,mail , fail_silently=False)

              resultset=[]
              resultset.append(randpass)
              resultset.append(mf.cleaned_data['email'])
              request.session['otppass']=resultset
              return render(request,'designers/passupdate.html',{})

          return render(request,'designers/forgotpass.html')


    return render(request,'designers/forgotpass.html',{})


def passmatch(request):
    if request.method=="POST":
        if request.session.has_key('otppass'):
            mfu=fppass(request.POST)
            if mfu.is_valid():



                if mfu.cleaned_data['otp']==request.session['otppass'][0]:
                    desu=Designers.objects.filter(email=request.session['otppass'][1])

                    desu.update(password=make_password(mfu.cleaned_data['password']))
                    print(mfu.cleaned_data['password'])
                    del request.session['otppass']
                    return render(request, 'designers/register.html',{})
                return render(request,'designers/passupdate.html',{})
        else:

            return render(request, 'designers/forgotpass.html',{})



def resendotp(request):

    if request.session.has_key('otppass'):
        if request.method == "POST":

            f=[]
            randpasss = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))  #otp
            f.append(request.session['otppass'][1])  #email

            print(randpasss)
            from_email = settings.EMAIL_HOST_USER
            send_mail('OTP', randpasss, from_email, f, fail_silently=False)
            l=[]
            l.append(randpasss)
            l.append(request.session['otppass'][1])


            request.session['otppass']=l

            return render(request, 'designers/passupdate.html', {})

    return render(request, 'designers/passupdate.html', {})





def test(request):
    return render(request, 'designers/test.html', {})


