from django.urls import path
from .views import RegisterView, ForgotPasswordView, ResetPasswordView,LogoutView,LoginView,SendOTPView,VerifyOTPView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
    path('auth/send-otp/', SendOTPView.as_view(), name="send-otp"),
    path('auth/verify-otp/', VerifyOTPView.as_view(), name="verify-otp"),
]
