from django.db import models
from .utils import set_image_tag, LocalizedModelBase


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
