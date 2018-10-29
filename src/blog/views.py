from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.postgres.search import SearchVector
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
#from haystack.query import SearchQuerySet
import markdown
# import the strip_tags
from django.utils.html import strip_tags
from django.utils.text import Truncator


from accounts.models import CustomUser
from .forms import  CommentForm, PostForm, SearchForm
from.models import Post, Category,Comment


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 15) # 9 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    context={'page': page, 'posts': posts,'tag': tag}
    return render(request, 'blog/post/list.html', context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,status='published',publish__year=year,publish__month=month, publish__day=day)
    
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    #print(Truncator(strip_tags(markdown.markdown(post.body))).words(2, truncate=''))
    context={'post': post, 'comments': comments,'comment_form': comment_form,'similar_posts': similar_posts}
    return render(request, 'blog/post/detail.html', context) 

def list_of_post_by_category(request, search_category):
    #categories = Category.objects.all()
    categories = Category.objects.filter(slug=search_category)
    if categories:
        category = categories[0]
        posts = Post.objects.filter(category=category, status='published')
    else:
        category = None
        posts = Post.objects.filter(status='published')
    context = {'posts':posts, 'category': category }
    return render(request, 'blog/category/list_of_post_by_category.html', context)


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.annotate(search=SearchVector('title', 'body'),).filter(search=query)
    return render(request,'blog/post/search.html',{'form': form,'query': query,'results': results})


