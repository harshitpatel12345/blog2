from django.contrib import admin
from blogging.models import User, Blog, Comment, Category
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm


# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    ordering = ("email",)
    search_fields = ("email",)
    list_display = ("email", "is_staff", "is_active")
    list_filter = ("email", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password", "image", "mobile")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")}
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "image",
                    "mobile",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at')
    search_fields = ('title', 'author__username', 'category__name')
    list_filter = ('author', 'category', 'created_at')
    ordering = ('-created_at',)


admin.site.register(Blog, BlogAdmin)
admin.site.register(Category)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user', 'created_at')
    # search_fields = ('blog__title', 'user__username', 'content')
    # list_filter = ('created_at',)
    # ordering = ('-created_at',)


admin.site.register(Comment, CommentAdmin)
