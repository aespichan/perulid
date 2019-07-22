from django.conf.urls import url
from . import views

app_name = 'lid'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^langid/', views.results, name='results'),
    url(r'^resources/', views.resources, name='resources'),
    url(r'^about/', views.about, name='about'),
    url(r'^contact/', views.contact, name='contact'),
    url(r'^ajax/search_sentences/', views.search_sentences, name='search_sentences'),
]