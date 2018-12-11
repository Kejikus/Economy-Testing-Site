from django.conf.urls import url
from django.urls import path, re_path
from django.contrib.auth.views import LoginView
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.attempts, name='attempts'),
    path(r'result/', views.result, name='result'),
    re_path(r'register/', views.register, name='register'),
    # path(r'login/', LoginView.as_view(template_name="login.html")),
]
