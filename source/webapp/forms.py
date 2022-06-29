from django import forms
from django.forms import widgets

from webapp.models import STATUS_CHOICES


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=50, required=True, label='Заголовок',
                            error_messages={"required": "Поле обязательно для заполнения"}, help_text="Введите заголовок")
    author = forms.CharField(max_length=50, required=True, label='Автор')
    content = forms.CharField(max_length=3000, required=True, label='Контент',
                              widget=widgets.Textarea(attrs={"cols": 40, "rows": 3}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, label="Статус")
