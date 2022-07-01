from datetime import date

from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import widgets

from webapp.models import STATUS_CHOICES, Article


# def publish_date_validate(value):
#     if value < date.today():
#         raise ValidationError("Дата публикации не должна быть раньше чем сегодня")


# class ArticleForm(forms.Form):
#     title = forms.CharField(max_length=50, required=True, label='Заголовок',
#                             error_messages={"required": "Поле обязательно для заполнения"},
#                             help_text="Введите заголовок")
#     author = forms.CharField(max_length=50, required=True, label='Автор')
#     content = forms.CharField(max_length=3000, required=True, label='Контент',
#                               widget=widgets.Textarea(attrs={"cols": 40, "rows": 3}))
#     status = forms.ChoiceField(choices=STATUS_CHOICES, label="Статус")
#     publish_date = forms.DateField(label="Дата публикации", required=False,
#                                    widget=widgets.DateInput(attrs={"type": "date"}),
#                                    )
#
#     def clean_publish_date(self):
#         if self.cleaned_data.get("publish_date") and self.cleaned_data.get("publish_date") < date.today():
#             raise ValidationError("Дата публикации не должна быть раньше чем сегодня")
#         return self.cleaned_data.get("publish_date")
#
#
#     def clean(self):
#         # return self.cleaned_data
#         return super().clean()

class ArticleForm(forms.ModelForm):
    title = forms.CharField(max_length=50, required=True, label='Заголовок',
                            error_messages={"required": "Поле обязательно для заполнения"},
                            help_text="Введите заголовок")

    class Meta:
        model = Article
        fields = "__all__"
        error_messages = {
            "title": {
                "required": "Поле обязательно для заполнения"
            }}
        widgets = {
            "publish_date": widgets.DateInput(attrs={"type": "date"})
        }
