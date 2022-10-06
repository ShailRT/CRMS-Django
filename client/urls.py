from django.urls import path 
from . import views
urlpatterns = [
    path('login/', views.client_login, name="client-login"),
    path('', views.dashboard, name="dashboard"),
    path('campaign/<str:pk>', views.campaign, name="client-campaign"),
    path('lead-pack/', views.lead_pack, name="lead-pack"),
    path('logout/', views.client_logout, name="client-logout")

]
