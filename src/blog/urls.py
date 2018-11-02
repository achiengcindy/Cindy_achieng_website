from django.urls import path,re_path 

from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    re_path(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',views.post_detail,name='post_detail'),
    #re_path(r'^update/$', views.post_update, name='post_update'),
    #re_path(r'^(?P<post_id>\d+)/share/$', views.post_share, name='post_share'),
    re_path(r'^feed/$', LatestPostsFeed(), name='post_feed'),
    re_path(r'^search/$', views.post_search, name='post_search'),
    re_path(r'^category/(?P<search_category>[-\w]+)/$', views.list_of_post_by_category, name='list_of_post_by_category')
]



