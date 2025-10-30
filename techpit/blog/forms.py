from django import forms
from .models import Blog


class BlogForm(forms.ModelForm):
    """
    新規データ登録画面用のフォーム定義
    """
    class Meta:
        model = Blog
        fields = ['title', 'content', 'category']
