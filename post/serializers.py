from rest_framework import serializers

from post.models import Post, PostTag


class PostTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTag
        fields = (
            "id",
            "name_en",
            "name_zh",
        )


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "title_en",
            "title_zh",
            "content_en",
            "content_zh",
            "media_en",
            "media_zh",
            "created_at",
            "updated_at",
            "tags",
        )

    tags = PostTagSerializer(many=True, read_only=True)
