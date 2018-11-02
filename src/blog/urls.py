from django.urls import path,re_path 

from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail,name='post_detail'),
    path('tag/<slug:tag_slug>/',views.post_list, name='post_list_by_tag'),
    path ('feeds/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
    re_path(r'^category/(?P<search_category>[-\w]+)/$', views.list_of_post_by_category, name='list_of_post_by_category')
]



