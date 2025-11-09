from django.db import models
from django.db.models.base import ModelBase
from .utils import localized_field


# Create your models here.
class LocalizedModelBase(ModelBase):
    """Metaclass to add localized fields to models during class creation.

    This processes the 'localized_fields' attribute which should be a list of tuples:
    (base_name, field_class, field_kwargs_dict)
    """

    def __new__(cls, name, bases, attrs, **kwargs):
        # Process localized_fields if present
        if "localized_fields" in attrs:
            field_configs = attrs.pop("localized_fields")
            for base_name, field_class, field_kwargs in field_configs:
                attrs.update(localized_field(base_name, field_class, **field_kwargs))
        return super().__new__(cls, name, bases, attrs, **kwargs)


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
