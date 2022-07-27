from django.db import models

# Create your models here.
from django.template.defaultfilters import slugify
from django.urls import reverse

from webapp.validate import validate_title


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        abstract = True


class Article(BaseModel):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Заголовок")
    author = models.CharField(max_length=50, verbose_name="Автор", default="Unknown")
    content = models.TextField(max_length=3000, verbose_name="Контент")
    tags = models.ManyToManyField("webapp.Tag", related_name="articles", blank=True)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return f"{self.id}. {self.title}: {self.author}"

    def get_absolute_url(self):
        return reverse("article_view", kwargs={"pk": self.pk})

    def upper(self):
        return self.title.upper()

    class Meta:
        db_table = "articles"
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     return super().save(*args, **kwargs)


class Comment(BaseModel):
    text = models.TextField(max_length=400, verbose_name='Комментарий')
    author = models.CharField(max_length=40, null=True, blank=True, default='Аноним', verbose_name='Автор')
    article = models.ForeignKey("webapp.Article", on_delete=models.CASCADE, related_name="comments",
                                verbose_name='Статья')

    def __str__(self):
        return f"{self.id}. {self.text}: {self.author}"

    class Meta:
        db_table = "comments"
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Tag(BaseModel):
    name = models.CharField(max_length=31, verbose_name='Тег')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tags"
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"
