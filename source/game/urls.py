from django.urls import path

from game.views import index_view, get_stat

urlpatterns = [
    path('', index_view),
    path('stat/', get_stat),
]