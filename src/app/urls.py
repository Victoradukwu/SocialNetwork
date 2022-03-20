
from django.urls import path

from . import views
urlpatterns = [
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/<id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/like/<post_id>/', views.like_post, name='like_post'),
    path('posts/unlike/<post_id>/', views.unlike_post, name='unlike_post')
]

