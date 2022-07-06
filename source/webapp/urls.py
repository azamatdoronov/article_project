from django.urls import path
from django.views.generic import TemplateView, RedirectView

from webapp.views import IndexView, create_article, ArticleView, UpdateArticle, delete_article, MyRedirectView

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('articles/', RedirectView.as_view(pattern_name="index")),
    path('articles/add/', create_article, name="create_article"),
    path('article/<int:pk>/', ArticleView.as_view(extra_context={"test": 5}), name="article_view"),
    path('article/<int:pk>/update/', UpdateArticle.as_view(), name="update_article"),
    path('article/<int:pk>/delete/', delete_article, name="delete_article"),
]
