from django.shortcuts import render

# Create your views here.
from webapp.models import Article, STATUS_CHOICES


def index_view(request):
    articles = Article.objects.order_by("-created_at")
    context = {"articles": articles}
    return render(request, "index.html", context)


def article_view(request):
    pk = request.GET.get("pk")
    article = Article.objects.get(pk=pk)
    return render(request, "article_view.html", {"article": article})


def create_article(request):
    if request.method == "GET":
        return render(request, "create.html", {"statuses": STATUS_CHOICES})
    else:
        title = request.POST.get("title")
        author = request.POST.get("author")
        content = request.POST.get("content")
        status = request.POST.get("status")
        new_article = Article.objects.create(title=title, author=author, content=content, status=status)
        context = {"article": new_article}
        return render(request, "article_view.html", context)
