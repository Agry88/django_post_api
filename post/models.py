from django.db import models

from .utils import LocalizedModelBase, set_image_tag


class PostTag(models.Model, metaclass=LocalizedModelBase):
    localized_fields = [
        ("name", models.CharField, {"max_length": 200}),
        ("slug", models.SlugField, {"unique": True}),
    ]

    def __str__(self):
        return (
            getattr(self, "name_en", "") or getattr(self, "name_zh", "") or "Untitled"
        )


class Post(models.Model, metaclass=LocalizedModelBase):
    # Define localized fields - similar to using locals().update(localized_field(...))
    # The metaclass will convert these to title_en, title_zh, content_en, content_zh, etc.
    localized_fields = [
        ("title", models.CharField, {"max_length": 200}),
        ("content", models.TextField, {}),
        (
            "media",
            models.ImageField,
            {"upload_to": "media/", "null": True, "blank": True},
        ),
    ]

    tags = models.ManyToManyField(
        PostTag, through="Post_PostTag", through_fields=("post", "tag")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Return title_en if available, otherwise return first available title
        return (
            getattr(self, "title_en", "") or getattr(self, "title_zh", "") or "Untitled"
        )

    def image_tag_en(self):
        return set_image_tag(self.media_en)

    def image_tag_zh(self):
        return set_image_tag(self.media_zh)


class Post_PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(PostTag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
