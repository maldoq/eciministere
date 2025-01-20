from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('analyse_list/', views.analyse_list, name='analyse_list'),
    path('analyse_detail/<str:idDem>/', views.analyse_detail, name='analyse_detail'),
    path('analyse_validation/<str:idDem>/', views.analyse_validation, name='analyse_validation'),
    path('analyse_rejection/<str:idDem>/', views.analyse_rejection, name='analyse_rejection'),
    path('confirmation_list/', views.confirmation_list, name='confirmation_list'),
    path('confirmation_detail/<str:idDem>/', views.confirmation_detail, name='confirmation_detail'),
    path('confirmation_validation/<str:idDem>/', views.confirmation_validation, name='confirmation_validation'),
]
