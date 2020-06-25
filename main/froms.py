from django import forms
from pagedown.widgets import PagedownWidget
from .models import Post


class PostForm(forms.ModelForm):
	content=forms.CharField(widget=PagedownWidget())
	class Meta:
		model=Post
		fields=['title','content','image','drafts']

	def clean_title(self):
		data=self.cleaned_data['title']
		if len(data) <5:
			raise forms.ValidationError('Too short')
		return data