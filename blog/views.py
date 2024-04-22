from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Post, CustomUser, Comment
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, AddComment, AddPostForm
from django.contrib import messages


# Create your views here.
@login_required
def index(request):
    posts = Post.published.all()
    return render(request, 'index.html', {"posts": posts})


@login_required
def post_detail(request, post_id):
    similar_posts = None
    post = Post.objects.get(id=post_id)
    comments = post.comments.all()
    post_tags = post.tags.all()
    similar_posts = Post.published.filter(tags__in=post_tags).exclude(pk=post_id).annotate(
        tag_count=Count("tags")).order_by("-tag_count")[:4]

    comment_form = AddComment()
    return render(request, 'posts/post_detail.html',
                  {"post": post, "comments": comments, "similar_posts": similar_posts, 'form': comment_form})


def user_creating(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST, files=request.FILES)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            new_user = CustomUser.objects.create_user(username=cd['username'], password=cd['password'],
                                                      email=cd['email'],
                                                      profile_photo=cd['profile_photo'], bio=cd['bio'],
                                                      first_name=cd['first_name'],
                                                      last_name=cd['last_name'])
            new_user.save()
            return HttpResponse("Your account has been created successfully")
        else:
            # Handle invalid form data (e.g., display errors)
            return render(request, 'authentication/user_registraion.html', {'form': user_form})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'authentication/user_registraion.html', {'form': user_form})


@login_required
def add_comment(request, post_id):
    post = Post.published.get(id=post_id)
    if request.method == "POST":
        form = AddComment(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("post_detail", post_id=post_id)


@login_required
def add_post(request):
    if request.method == "POST":
        form = AddPostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            messages.success(request, 'Post added successfully!')  # Display success message
            return redirect('post_detail', post_id=new_post.id)  # Redirect to post detail page
        else:
            messages.error(request, 'Error adding post. Please check your input.')  # Display error message
    else:
        form = AddPostForm()  # Create a new form instance for GET requests

    return render(request, 'posts/add_post.html', {'form': form})


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        comment.delete()
        return redirect("post_detail", post_id=post_id)


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()

        return redirect('index')
