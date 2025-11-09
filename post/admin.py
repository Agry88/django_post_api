from django.contrib import admin
from .models import Post


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title_en", "title_zh", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("title_en", "title_zh", "content_en", "content_zh")

    fieldsets = (
        ("English", {"fields": ("title_en", "content_en", "media_en", "image_tag_en")}),
        ("Chinese", {"fields": ("title_zh", "content_zh", "media_zh", "image_tag_zh")}),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
    readonly_fields = ("created_at", "updated_at", "image_tag_en", "image_tag_zh")
