from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from designers.models import Designers,Blogs,Comments,BlogLiked
from .serializers import *
from django.contrib.auth.hashers import make_password,check_password

from designers.models import Designers
from store.models import VerifiedDesigners
from . serializers import DesignerSerializer, DesignerLogin, Register


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class IndexViewSet(APIView):
     authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
     @csrf_exempt
     def get(self,request,format=None):
         serialisers = DesignerLogin([])
         return Response(serialisers.data)

     @csrf_exempt
     def post(self,request,format=None):
        designerSe=Register(data=request.data)
        if designerSe.is_valid():
            designerSe.save()
            return Response(data=request.data, status=status.HTTP_202_ACCEPTED)


class Login(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(Login,self).dispatch(request)
    @csrf_exempt
    def get(self, request, format=None):
        serialisers = DesignerLogin([])
        return Response({})
    @csrf_exempt
    def post(self, request, format=None):
        serializer = DesignerLogin(data=request.data)
        print(request.data)
        if serializer.is_valid():
            designerID = serializer.data['designerID']
            user=Designers.objects.filter(designerID=designerID)
            password = serializer.data['password']
            dbuser = Designers.objects.filter(designerID=designerID)
            if dbuser and check_password(password, dbuser[0].password):
                user = dbuser[0]
                # profilepic = user.profilepic.url
                request.session['designerID'] = designerID
                user = DesignerSerializer(dbuser[0])
                request.session['id'] = user.data['email']
            designer = Designers.objects.filter(designerID=designerID)

            if designer and check_password(password, designer[0].password):
                user=DesignerSerializer(designer[0])
                return Response(user.data, status=status.HTTP_202_ACCEPTED)



            else:
                return Response("Not user", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SearchBlogs(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(SearchBlogs, self).dispatch(request)

    @csrf_exempt
    def post(self,request, *args, **kwargs):
        print(request.data)
        serialisers = BlogSearchForm(data=request.data)
        blogList = []
        print('hello')
        if serialisers.is_valid():
            blogList = []
            searchfield = list(set(serialisers.data['searchfield'].split(sep=" ")))

            for x in searchfield:
                newBlogs = Blogs.objects.filter(title__contains=x).order_by('-day','likes','shares')
                print(len(newBlogs))
                if len(newBlogs) < 3 and len(newBlogs) > 0:
                    blogList.extend(newBlogs)
                    blogList = list(set(blogList))
                newBlogs1 = Blogs.objects.filter(subject__contains=x).order_by('-day','likes','shares')
                if len(newBlogs1) < 3 and len(newBlogs1) > 0:
                    blogList.extend(newBlogs1)
                    blogList = list(set(blogList))
                    blog=BlogSerialisers(blogList[0])

                    res={}
                    count=1
                    for x in blogList:
                        key='blog{}'.format(count)
                        count=count+1
                        res[key]=BlogSerialisers(x).data
                        res[key]['comments']=CommentsSerialiser(Comments.objects.filter(blogID=x.id),many=True).data
                        res[key]['like']=LikesSerialiser(BlogLiked.objects.filter(blogID=x.id),many=True).data

                    return Response(res,status=status.HTTP_202_ACCEPTED)



        return Response(serialisers.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateBlog(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(CreateBlog, self).dispatch(request)

    @csrf_exempt
    def post(self,request, *args, **kwargs):
        if request.session.has_key('designerID'):
            form=CreateBLogsSerialiser(data=request.data)
            if form.is_valid():
                print(form.data)
                title=form.data['title']
                subject=form.data['subject']
                image=form.validated_data['image']
                blog=Blogs(title=title,subject=subject,image=image,author=Designers.objects.filter(designerID=request.session['designerID'])[0])
                print(blog)
                blog.save()
                return Response({},status=status.HTTP_201_CREATED)
            return Response(form.errors,status=status.HTTP_205_RESET_CONTENT)
        return Response({},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    @csrf_exempt
    def get(self,request,*args,**kwargs):
        if request.session.has_key('designerID'):
            form=BlogSerialisers(Blogs.objects.filter(author=Designers.objects.filter(designerID=request.session['designerID'])[0]).order_by('-day'),many=True)

            return Response(form.data,status=status.HTTP_200_OK)
        return  Response({},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)



class DesignerBlogs(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(DesignerBlogs, self).dispatch(request)
    @csrf_exempt
    def get(self,request,*args,**kwargs):
        if request.session.has_key('designerID'):

            blogs=list(Blogs.objects.all().order_by('-day'))
            res = {}
            count = 0
            for x in blogs:

                count = count + 1
                key = 'blog{}'.format(count)
                res[key] = BlogSerialisers(x).data
                res[key]['comment'] = CommentsSerialiser(Comments.objects.filter(blogID=x.id), many=True).data
                res[key]['like'] = LikesSerialiser(BlogLiked.objects.filter(blogID=x.id), many=True).data

            return Response(res, status=status.HTTP_200_OK)


        return  Response({},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    @csrf_exempt
    def post(self,request,*args,**kwargs):
        if request.session.has_key('designerID'):
            form = CommentCreate(data=request.data)
            if form.is_valid():
                body=form.data['body']
                blogID=form.data['blogID']
                print(blogID)
                blogs = Blogs.objects.filter(id=blogID)
                comments=blogs[0].comments+1
                comment = Comments(body=body, commenter=request.session['designerID'], blogID=blogID,
                                   commentedTo=blogs[0].author,
                                   author=Designers.objects.filter(designerID=request.session['designerID'])[0].name)
                comment.save()
                Blogs.objects.filter(id=blogID).update(comments=comments)
                return Response({}, status=status.HTTP_201_CREATED)
            return Response(form.errors, status=status.HTTP_205_RESET_CONTENT)
        return Response({}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

class LikeView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(LikeView, self).dispatch(request)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if request.session.has_key('designerID'):

            form = LikeCreate(data=request.data)
            if form.is_valid():
                blog = Blogs.objects.filter(id=form.data['values'])
                likes=blog[0].likes+1
                likecheck = BlogLiked.objects.filter(likedBy=request.session['designerID'], likedTo=blog[0].author,
                                                     blogID=blog[0].id)
                print(blog[0].id)

                if not likecheck:
                    like = BlogLiked(likedBy=request.session['designerID'], likedTo=blog[0].author, blogID=blog[0].id)
                    like.save()
                    Blogs.objects.filter(id=form.data['values']).update(likes=likes)

                    return Response({}, status=status.HTTP_201_CREATED)
                return Response({}, status=status.HTTP_201_CREATED)
            return Response(form.errors, status=status.HTTP_205_RESET_CONTENT)

        return Response({}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class Logout(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(Logout, self).dispatch(request)

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        try:
            del request.session['designerID']
        except:
            pass
        return Response({},status=status.HTTP_200_OK)













class StoreLogin(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @csrf_exempt
    def post(self, request, format=None):
        serializer = DesignerLogin(data=request.data)

        if serializer.is_valid():
            designerID = serializer.data['designerID']
            password = serializer.data['password']
            designer = Designers.objects.filter(designerID=designerID)

            if designer and check_password(password, designer[0].password):
                vdes = VerifiedDesigners.objects.filter(designer=designer[0])

                if vdes:

                    if vdes[0].verified:
                        return Response("Logged in successfully", status=status.HTTP_202_ACCEPTED)

                    return Response("Not a verified designer", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

                VerifiedDesigners.objects.create(designer=designer[0])
                return Response("Not a verified designer", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

            return Response("Not a user", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
