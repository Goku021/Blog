from django import forms
from .models import CustomUser, Comment, Post


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'password', 'email', 'date_of_birth', 'profile_photo', 'bio']


class AddComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']


class AddPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body', 'status', 'tags']


