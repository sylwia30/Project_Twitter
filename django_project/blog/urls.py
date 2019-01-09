from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostView,
    CommentCreateView,
    # CommentListView,
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    # path('', CommentListView.as_view(), name='blog-home'),
    path('user/<str:username>/', UserPostView.as_view(), name='user-post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('comment/', CommentCreateView.as_view(), name='comment-create'),

    path('about/', views.About.as_view(), name='blog-about'),
]