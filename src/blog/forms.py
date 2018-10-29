from django import forms
from .models import Comment
from .models import Post

 #creating model forms   
class CommentForm(forms.ModelForm):
    class Meta:
       model = Comment
       fields = ('website','body',)

class SearchForm(forms.Form):
	query = forms.CharField() 

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'image', 'body',)

