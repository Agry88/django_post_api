# Create your views here.
from drf_yasg import openapi
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
    - GET /api/posts/?tag_include=1,2 - Filter posts by tag IDs
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def handle_tag_include(self, queryset):
        tag_include = self.request.query_params.get("tag_include", None)
        if not tag_include:
            return queryset
        tag_ids = [
            int(tag_id.strip())
            for tag_id in tag_include.split(",")
            if tag_id.strip().isdigit()
        ]
        if tag_ids:
            queryset = queryset.filter(tags__id__in=tag_ids).distinct()
        return queryset

    def get_queryset(self):
        """
        Optionally restricts the returned posts by filtering against
        a `tag_include` query parameter in the URL.
        """
        queryset = self.queryset
        queryset_handle_pipe_line = [
            self.handle_tag_include,
        ]
        for handler in queryset_handle_pipe_line:
            queryset = handler(queryset)
        return queryset

    @swagger_auto_schema(
        operation_summary="Retrieve all posts",
        operation_description="Retrieve all posts. Optionally filter by tags using ?tag_include=1,2",
        manual_parameters=[
            openapi.Parameter(
                "tag_include",
                openapi.IN_QUERY,
                description="Comma-separated list of tag IDs to filter posts (e.g., 1,2)",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
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
