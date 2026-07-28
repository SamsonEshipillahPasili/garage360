from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),
    path('clients/create', views.CreateClientView.as_view(), name='create_client'),
    path('clients/list', views.ListClientsView.as_view(), name='list_clients'),
]
