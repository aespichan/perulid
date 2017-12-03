from django.conf.urls import url
from . import views

app_name = 'lid'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^langid/', views.results, name='results'),
    url(r'^resources/', views.resources, name='resources'),
    url(r'^ajax/search_sentences/', views.search_sentences, name='search_sentences'),
]