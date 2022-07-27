from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.template.defaultfilters import slugify

from webapp.models import Article, Comment


class UserArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title"]


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "author", "content", "tags"]
        widgets = {
            "tags": widgets.CheckboxSelectMultiple,
            "content": widgets.Textarea(attrs={"placeholder": "введите контент"})
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        if title == cleaned_data.get("content"):
            raise ValidationError("Название и описание не могут совпадать")
        if Article.objects.filter(title=title).exists():
            raise ValidationError("Статья с таким названием уже существует")
        return cleaned_data

    def save(self, commit=True):
        article = super().save(False)
        article.slug = slugify(article.title)
        article.save()
        return article

class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Найти')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text", "author"]


class ArticleDeleteForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title"]

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if self.instance.title != title:
            raise ValidationError("Названия не совпадают")
        return title
