from django.shortcuts import render
from blog.models import Post
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404,redirect

def home(request):
    context = {}
    return render(request, 'home/home.html', context)

def permalink(request, id):
    post = get_object_or_404(Post, id=id)
    return HttpResponseRedirect(post.get_absolute_url())
