from django.contrib import admin

from .models import Post, Post_PostTag, PostTag


# Register your models here.
class Post_PostTagInline(admin.TabularInline):
    model = Post_PostTag
    extra = 0
    autocomplete_fields = ("tag",)
    verbose_name = "Tag"


class PostTag_PostInline(admin.TabularInline):
    model = Post_PostTag
    extra = 0
    autocomplete_fields = ("post",)
    verbose_name_plural = "Posts"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title_en", "title_zh", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("title_en", "title_zh", "content_en", "content_zh")
    inlines = [Post_PostTagInline]

    fieldsets = (
        ("English", {"fields": ("title_en", "content_en", "media_en", "image_tag_en")}),
        ("Chinese", {"fields": ("title_zh", "content_zh", "media_zh", "image_tag_zh")}),
        (
            "Metadata",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "image_tag_en",
        "image_tag_zh",
    )


@admin.register(PostTag)
class PostTagAdmin(admin.ModelAdmin):
    list_display = ("name_en", "name_zh", "slug_en", "slug_zh")
    search_fields = ("name_en", "name_zh", "slug_en", "slug_zh")
    inlines = [PostTag_PostInline]
