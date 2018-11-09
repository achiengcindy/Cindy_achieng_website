from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from taggit.managers import TaggableManager


class Category(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,  unique=True)
     
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('blog:list_of_post_by_category', args=[self.slug])   

    def __str__(self):
        return self.title

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    category = models.ForeignKey(Category, default="",on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blog_posts',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    caption = models.URLField(max_length=250,null=True, blank=True)
    alt = models.CharField(max_length=250, default = '')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager() # The default manager.
    published = PublishedManager() # The Dahl-specific manager.


    tags = TaggableManager()

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = ('-publish',)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug]) 

    def get_permalink_url(self):
        return reverse('permalink', args=[self.id])    

class Comment(models.Model):

    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='user_comments',on_delete=models.CASCADE, default='')
    website = models.URLField(null=True, blank=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {}'.format(self.commenter)
  






