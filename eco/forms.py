from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
		class Meta:
				model = Article
				fields = ('title', 'body', 'date', 'author', 'diy_package', 'package_quantity', 'diy_files')
