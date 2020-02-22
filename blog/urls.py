from django.urls import path
from .views import PostListView,PostDetailView,SharePostView
from .feeds import LatestPostsFeed

urlpatterns = [
    path('feed/',LatestPostsFeed(),name='posts_feed'),
    path('',PostListView.as_view(),name='home'),
    path('posts/<str:tag>/',PostListView.as_view(),name='home_with_tag'),
    path('posts/<str:slug>/share/',SharePostView.as_view(),name='post-share'),
    path('posts/<str:slug>/detail/',PostDetailView.as_view(),name='post-detail'),
]