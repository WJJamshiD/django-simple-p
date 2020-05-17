from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','content','image']

    def clean_title(self):
        data=self.cleaned_data['title']
        if len(data) <5:
            raise forms.ValidationError('Too short')
        return data