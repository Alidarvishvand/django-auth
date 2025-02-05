from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from yaml import serialize
from .serializers import RegisterSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from .models import OTP
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer,SendOTPSerializer,VerifyOTPSerializer
import random
from django.contrib.auth import logout
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import OTP, CustomUser
from .utils import send_otp_kavenegar


class RegisterView(APIView):
    serializer_class = RegisterSerializer  
    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={201: "ثبت‌نام موفق", 400: "خطای درخواست"}
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)  
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "ثبت‌نام موفق", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    serializer_class = LoginSerializer  
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: "ورود موفق", 400: "خطای احراز هویت"}
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "ورود موفق",
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
    
class ForgotPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer  
    
    @swagger_auto_schema(
        request_body=ForgotPasswordSerializer,
        responses={200: "کد OTP ارسال شد", 400: "خطا در درخواست"}
    )
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            otp_code = str(random.randint(100000, 999999))
            OTP.objects.update_or_create(phone_number=phone_number, defaults={"otp_code": otp_code})
            return Response({"message": "کد OTP ارسال شد"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer
    @swagger_auto_schema(
        request_body=ResetPasswordSerializer,
        responses={200: "رمز عبور تغییر کرد", 400: "خطا در درخواست"}
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "رمز عبور با موفقیت تغییر یافت"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class VerifyOTPView(APIView):
    @swagger_auto_schema(
        request_body=VerifyOTPSerializer,
        responses={
            200: "ورود موفق با توکن JWT.",
            400: "کد OTP نامعتبر است یا منقضی شده است."
        }
    )
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]


            OTP.objects.filter(phone_number=phone_number).delete()


            user, created = CustomUser.objects.get_or_create(phone_number=phone_number)


            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "ورود موفق",
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









class SendOTPView(APIView):
    @swagger_auto_schema(
        request_body=SendOTPSerializer,
        responses={
            200: "کد OTP ارسال شد.",
            400: "شماره موبایل نامعتبر است.",
            500: "خطا در ارسال کد."
        }
    )
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]


            otp_code = str(random.randint(100000, 999999))

            OTP.objects.update_or_create(phone_number=phone_number, defaults={"otp_code": otp_code})


            if send_otp_kavenegar(phone_number, otp_code):
                return Response({"message": "کد OTP ارسال شد."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "مشکلی در ارسال کد پیش آمد."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  

    @swagger_auto_schema(responses={200: "خروج موفق"})
    def post(self, request):
        logout(request)  
        return Response({"message": "خروج موفق"}, status=200)