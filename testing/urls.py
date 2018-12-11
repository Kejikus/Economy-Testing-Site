from django.conf.urls import url
from django.urls import path, re_path
from django.views.generic import RedirectView
from . import views

app_name = 'testing'

urlpatterns = [
    path('', views.testing, name='testing'),
    path('results/', views.results, name='results'),
    # url(r'^results', views.show_results, name='results'),
]
