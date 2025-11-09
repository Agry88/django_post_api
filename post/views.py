# Create your views here.
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from post.models import Post
from post.serializers import PostSerializer


# Create your views here.
class PostViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
