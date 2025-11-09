# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from post.models import Post
from post.serializers import PostSerializer


# Create your views here.
class PostViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    ViewSet for managing Post objects.

    Provides:
    - GET /api/posts/ - Retrieve all posts
    - GET /api/posts/{id}/ - Retrieve a specific post
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @swagger_auto_schema(
        operation_summary="Retrieve all posts",
        operation_description="Retrieve all posts",
        responses={
            200: PostSerializer(many=True),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a post",
        operation_description="Retrieve a specific post by its ID",
        responses={
            200: PostSerializer,
            404: "Not Found - Post does not exist",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
