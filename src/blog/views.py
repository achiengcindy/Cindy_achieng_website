from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from.models import Post
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags
from django.utils.text import Truncator

from accounts.models import CustomUser

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,status='published',publish__year=year,publish__month=month, publish__day=day)
    
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    #print(Truncator(strip_tags(markdown.markdown(post.body))).words(2, truncate=''))
    context={'post': post}
    return render(request, 'blog/post/detail.html', context) 