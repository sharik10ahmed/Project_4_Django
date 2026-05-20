from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path('', views.home, name='home'),

    path('login/', views.custom_login, name='login'),

    path('logout/', LogoutView.as_view(), name='logout'),

    path('register/', views.register_user, name='register'),

    path('create/', views.create_product, name='create_product'),

    path('edit/<int:id>/', views.edit_product, name='edit_product'),

    path('delete/<int:id>/', views.delete_product, name='delete_product'),

    path('profile/', views.profile_view, name='profile'),

    path(
        'edit-profile/',
        views.edit_profile,
        name='edit_profile'
    ),

    path(
        'delete-account/',
        views.request_delete_account,
        name='delete_account'
    ),

    path(
        'delete-account-confirm/<uidb64>/<token>/',
        views.confirm_delete_account,
        name='confirm_delete_account'
    ),
]