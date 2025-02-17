from django.urls import path

from . import views

urlpatterns = [
    path('', views.guest_home, name='home'),
    path('about/', views.guest_about, name='about'),
    path('contact/', views.guest_contact, name='contact'),
    path('demande/', views.demand_list, name='demandelist'),
    path('demande/add', views.add_demand, name='add_demand'),
    path('demandes/<str:idDem>/', views.show_demand, name='show_demand'),  # Show details of a specific demand
    path('demandes/edit/<str:idDem>/', views.edit_demand, name='edit_demand'),  # Edit an existing demand
    path('profile/', views.profile_user, name='profile_view'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('notification/',views.notif_user, name='notification'),
]
