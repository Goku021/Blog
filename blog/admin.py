from django.contrib import admin
from .models import CustomUser, Post, Comment


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'email', 'date_of_birth']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'body', 'status', 'author']
    list_filter = ['status', 'author', 'publish', 'created']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['body', 'author', 'body']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'body']
