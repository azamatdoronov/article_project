from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404
from django.urls import reverse

# Create your views here.
from webapp.forms import ArticleForm
from webapp.models import Article
from webapp.validate import article_validate


def index_view(request):
    articles = Article.objects.order_by("-updated_at")
    context = {"articles": articles}
    return render(request, "index.html", context)


def article_view(request, **kwargs):
    pk = kwargs.get("pk")
    article = get_object_or_404(Article, pk=pk)
    return render(request, "article_view.html", {"article": article})


def create_article(request):
    if request.method == "GET":
        form = ArticleForm()
        return render(request, "create.html", {"form": form})
    else:
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            author = form.cleaned_data.get("author")
            content = form.cleaned_data.get("content")
            status = form.cleaned_data.get("status")
            new_article = Article.objects.create(title=title, author=author, content=content, status=status)
            return redirect("article_view", pk=new_article.pk)
        return render(request, "create.html", {"form": form})


def update_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "GET":
        form = ArticleForm(initial={
            "title": article.title,
            "author": article.author,
            "content": article.content,
            "status": article.status
        })
        return render(request, "update.html", {"form": form})
    else:
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article.title = form.cleaned_data.get("title")
            article.author = form.cleaned_data.get("author")
            article.content = form.cleaned_data.get("content")
            article.status = form.cleaned_data.get("status")
            article.save()
            return redirect("article_view", pk=article.pk)
        return render(request, "update.html", {"form": form})


def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "GET":
        pass
    #     return render(request, "delete.html", {"article": article})
    else:
        article.delete()
        return redirect("index")
