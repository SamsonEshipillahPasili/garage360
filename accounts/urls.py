from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login', views.AuthLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('profile/create', views.CreateUserProfileView.as_view(), name='create_profile'),
    path('profiles', views.ListProfilesView.as_view(), name='list_profiles'),
    path('profiles/edit/<int:pk>', views.EditProfileView.as_view(), name='edit_profile'),
]
