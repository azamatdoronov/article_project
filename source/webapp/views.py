from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views import View

from webapp.forms import ArticleForm, SearchForm
from webapp.models import Article
from django.views.generic import TemplateView, RedirectView


class IndexView(View):
    def get(self, request, *args, **kwargs):
        create_article_form = ArticleForm()
        return index_view_partial(request, create_article_form)


class MyRedirectView(RedirectView):
    url = "https://www.google.ru/"


class ArticleView(TemplateView):
    template_name = "article_view.html"

    def get_context_data(self, **kwargs):
        pk = kwargs.get("pk")
        article = get_object_or_404(Article, pk=pk)
        kwargs["article"] = article
        return super().get_context_data(**kwargs)


def index_view_partial(request, create_article_form):
    search_form = SearchForm(data=request.GET)
    articles = Article.objects.all()
    if search_form.is_valid():
        search_value = search_form.cleaned_data.get("search")
        articles = articles.filter(title__contains=search_value)
    articles = articles.order_by("-updated_at")
    context = {"articles": articles, "search_form": search_form, "create_article_form": create_article_form}
    return render(request, "index.html", context)


def create_article(request):
    if request.method == "POST":
        create_article_form = ArticleForm(data=request.POST)
        if create_article_form.is_valid():
            title = create_article_form.cleaned_data.get("title")
            author = create_article_form.cleaned_data.get("author")
            content = create_article_form.cleaned_data.get("content")
            new_article = Article.objects.create(title=title, author=author, content=content)
            return redirect("article_view", pk=new_article.pk)
        return index_view_partial(request, create_article_form)


class UpdateArticle(View):

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        self.article = get_object_or_404(Article, pk=pk)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # pk = kwargs.get("pk")
        # article = get_object_or_404(Article, pk=pk)
        if request.method == "GET":
            form = ArticleForm(initial={
                "title": self.article.title,
                "author": self.article.author,
                "content": self.article.content
            })
            return render(request, "update.html", {"form": form})

    def post(self, request, *args, **kwargs):
        # pk = kwargs.get("pk")
        # article = get_object_or_404(Article, pk=pk)
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            self.article.title = form.cleaned_data.get("title")
            self.article.author = form.cleaned_data.get("author")
            self.article.content = form.cleaned_data.get("content")
            self.article.save()
            return redirect("article_view", pk=self.article.pk)
        return render(request, "update.html", {"form": form})


def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "GET":
        pass
    #     return render(request, "delete.html", {"article": article})
    else:
        article.delete()
        return redirect("index")
