# Create your views here.
from drf_yasg.utils import status, swagger_auto_schema
from rest_framework.views import Response
from rest_framework.viewsets import GenericViewSet

from post.models import Post
from post.serializers import PostSerializer


# Create your views here.
class PostViewSet(GenericViewSet):
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
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Retrieve a post",
        operation_description="Retrieve a specific post by its ID",
        responses={
            200: PostSerializer,
            404: "Not Found - Post does not exist",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
