from django.urls import path
from .views import PostListView,PostDetailView,SharePostView
from .feeds import LatestPostsFeed

urlpatterns = [
    path('',PostListView.as_view(),name='home'),
    path('<str:tag>/',PostListView.as_view(),name='home_with_tag'),
    path('<str:slug>/share/',SharePostView.as_view(),name='post-share'),
    path('<str:slug>/detail/',PostDetailView.as_view(),name='post-detail'),
    path('feed/',LatestPostsFeed(),name='posts_feed')
]