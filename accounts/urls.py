from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('register/', views.register,name='register'),
    path('login/', views.login,name='login'),
    path('logout/', views.logout_view,name='logout'),
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='auth/password_reset_form.html'), name='password-reset'),
    path('password-reset-done/',auth_view.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
]