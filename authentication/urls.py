from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_people, name='register_people'),
    path('login/', views.login_view, name='login'),
]