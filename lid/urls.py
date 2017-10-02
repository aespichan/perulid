from django.conf.urls import url
from . import views

app_name = 'lid'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^langid/', views.results, name='results'),
]