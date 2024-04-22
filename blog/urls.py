from django.urls import path
from django.contrib.auth.views import LogoutView,LoginView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("<int:post_id>/", views.post_detail, name='post_detail'),
    path('logout/', LogoutView.as_view(template_name='authentication/logged_out.html'), name='logout'),
    path('login/',LoginView.as_view(template_name='authentication/logged_in.html'), name='login'),
    path('register/', views.user_creating, name='register_new_user'),
    path("<int:post_id>/comment/", views.add_comment, name='add_comment'),
    path("add_post/", views.add_post, name='add_post'),
    path("<int:post_id>/delete_comment/<int:comment_id>/", views.delete_comment, name='delete_comment'),
    path("<int:post_id>/delete/", views.post_delete, name='delete_post')
]
