from django.contrib import admin
from .models import Post , Comment, Category

class PostAdmin(admin.ModelAdmin):
	list_display =('title','slug','author','publish', 'status')
	list_filter =('status','created','publish','author')
	search_fields=('title','body')
	prepopulated_fields={'slug':('title',),}
	raw_id_fields=('author',)
	date_hierarchy='publish'
	ordering=['status','publish']
	#list_editable =['title']
	#list_display_links =['updated']


class CategoryAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug')
	prepopulated_fields = {'slug':('title',)}

class CommentAdmin(admin.ModelAdmin):
	list_display = ( 'post', 'created', 'active')
	list_filter = ('active', 'created', 'updated')
	search_fields = ('body', 'website')
	


   
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)


