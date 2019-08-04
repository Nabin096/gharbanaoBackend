from designers.models import Designers,Blogs,Comments,BlogLiked
from rest_framework import serializers


class DesignerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designers
        fields='__all__'


class DesignerLogin(serializers.Serializer):
    designerID=serializers.CharField(max_length=100)
    password=serializers.CharField(max_length=100)


class Register(serializers.ModelSerializer):
    class Meta:
        model = Designers
        fields=('name','firmname','contact','address','email')

class BlogSearchForm(serializers.Serializer):
    searchfield=serializers.CharField(max_length=1000)


class BlogSerialisers(serializers.ModelSerializer):
    class Meta:
        model=Blogs
        fields='__all__'

class CreateBLogsSerialiser(serializers.Serializer):
    title = serializers.CharField(max_length=25)
    subject = serializers.CharField(max_length=1000)
    image = serializers.ImageField(required=False)

class CommentsSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields=('body','author')


class LikesSerialiser(serializers.Serializer):
    class Meta:
        model=BlogLiked
        fields=('likedBy','blogID')


class CommentCreate(serializers.Serializer):
    body=serializers.CharField(max_length=100)
    blogID=serializers.IntegerField()


class LikeCreate(serializers.Serializer):
    values=serializers.IntegerField()

class StoreLogin(serializers.Serializer):
    pass
