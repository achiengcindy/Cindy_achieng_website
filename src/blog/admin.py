from django.contrib import admin

from .models import Post, Category

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display =('title','slug','author','publish', 'status')
	list_filter =('status','created','publish','author')
	search_fields=('title','body')
	prepopulated_fields={'slug':('title',),}
	raw_id_fields=('author',)
	date_hierarchy='publish'
	ordering=['status','publish']

""" @admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('commenter', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('commenter', 'body')
 """
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug')
	prepopulated_fields = {'slug':('title',)}
