from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('validate-firstname', csrf_exempt(views.FirstnameValidationView.as_view()), name="validate-firstname"),
    path('validate-lastname', csrf_exempt(views.LastnameValidationView.as_view()), name="validate-lastname"),
    path('validate-username', csrf_exempt(views.UsernameValidationView.as_view()), name="validate-username"),
    path('validate-email', csrf_exempt(views.EmailValidationView.as_view()), name="validate-email"),
    path('activate/<uidb64>/<token>', views.VerificationView.as_view(), name="activate"),
    # password reset
    path('reset-password', views.EmailPasswordResetView.as_view(), name="reset-password"),
    path('set-newpassword/<uidb64>/<token>', views.CompletePasswordResetView.as_view(), name="set-newpassword"),
    # path('password-reset/', auth_views.PasswordResetView.as_view(template_name="authentication/reset_password.html"), name='password_reset'),
    # path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name="authentication/reset_password_done.html"), name="password_reset_done"),
    # path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="authentication/set_newpassword.html"), name="password-reset_confirm"),
    # path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name="authentication/reset_password_complete.html"), name="password_reset_complete"),
]
