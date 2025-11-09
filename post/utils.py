from django.conf import settings
from django.db import models
from django.utils.html import format_html
from django.db.models.base import ModelBase


def localized_field(base_name, field_class=models.CharField, **kwargs):
    """
    Dynamically create localized fields for a model.

    Args:
        base_name: Base name for the field (e.g., 'title')
        field_class: Django field class to use (default: CharField)
        **kwargs: Additional arguments to pass to the field class

    Returns:
        dict: Dictionary of field_name -> field_instance mappings
    """
    fields = {}
    for lang, _ in settings.LANGUAGES:
        # Extract language code (e.g., 'zh-hant' -> 'zh')
        lang_code = lang.split("-")[0] if "-" in lang else lang
        field_name = f"{base_name}_{lang_code}"
        fields[field_name] = field_class(**kwargs)
    return fields


def set_image_tag(media_field: str) -> str:
    """Helper method to generate image tag HTML for a given media field."""
    if media_field:
        return format_html(
            '<img src="{}" style="width: 100%;" />',
            media_field.url,
        )
    return "No image"


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
