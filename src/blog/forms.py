from django import forms
# from .models import Comment
from .models import Post

class EmailPostForm(forms.Form):
    name=forms.CharField(required=False, max_length=100)
    email=forms.EmailField(required=True)
    to = forms.EmailField()
    comments = forms.CharField(required=True, widget=forms.Textarea)	

"""  #creating model forms   
class CommentForm(forms.ModelForm):
    class Meta:
       model = Comment
       fields = ('website','body',)
 """
class SearchForm(forms.Form):
	query = forms.CharField() 

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'image', 'body',)

