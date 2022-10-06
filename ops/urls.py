from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('signin/', views.signin, name='signin'),
    path('table/', views.table, name='table'),
    path('campaign/<str:pk>/', views.campaign, name='campaign'),
    path('push/<str:pk>/', views.push, name='push'),
    path('push-history/', views.push_history, name='push-history'),
    path('logout/', views.logout, name='logout'),
    
    path('camp-create/', views.camp_create, name='camp-create'),

    path('lead-create/<str:pk>/', views.create_lead, name='create-lead'),
    path('heap-push/', views.heap_upload, name='heap-push'),
]
