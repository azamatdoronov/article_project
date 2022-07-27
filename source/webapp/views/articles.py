from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse_lazy

from webapp.forms import ArticleForm, ArticleDeleteForm, UserArticleForm
from webapp.models import Article
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from webapp.views import SearchView


class IndexView(SearchView):
    model = Article
    template_name = "articles/index.html"
    context_object_name = "articles"
    ordering = "-updated_at"
    paginate_by = 5
    search_fields = ["title__contains", "author__contains"]


class ArticleView(DetailView):
    template_name = "articles/article_view.html"
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.object.comments.order_by("-created_at"), 2)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class CreateArticle(CreateView):
    form_class = ArticleForm
    template_name = "articles/create.html"

    def form_valid(self, form):
        article = form.save(commit=False)
        article.save()
        form.save_m2m()
        return redirect("article_view", pk=article.pk)


class UpdateArticle(UpdateView):
    form_class = ArticleForm
    template_name = "articles/update.html"
    model = Article

    def get_form_class(self):
        if self.request.GET.get("is_admin"):
            return ArticleForm
        return UserArticleForm


class DeleteArticle(DeleteView):
    model = Article
    template_name = "articles/delete.html"
    success_url = reverse_lazy('index')
    form_class = ArticleDeleteForm

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(data=request.POST, instance=self.get_object())
    #     if form.is_valid():
    #         return self.delete(request, *args, **kwargs)
    #     else:
    #         return self.get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == "POST":
            kwargs['instance'] = self.get_object()
        return kwargs
