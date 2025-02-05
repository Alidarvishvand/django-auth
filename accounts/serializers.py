from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import OTP,CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'username', 'password', 'confirm_password'] 

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password': 'رمز عبور و تکرار آن مطابقت ندارند.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser(
            phone_number=validated_data['phone_number'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'error': 'کاربری با این شماره یافت نشد.'})

        if not user.check_password(password):
            raise serializers.ValidationError({'error': 'رمز عبور نادرست است.'})

        attrs['user'] = user
        return attrs
    
    
    
    
    
class ForgotPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    
    def validate_phone_number(self, value):
        if not CustomUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError('کاربری با این شماره تلفن یافت نشد.')
        return value

class ResetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp_code = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)
    
    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        otp_code = attrs.get('otp_code')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        
        if new_password != confirm_password:
            raise serializers.ValidationError({'password': 'رمز عبور و تکرار آن مطابقت ندارند.'})
        
        if not OTP.objects.filter(phone_number=phone_number, otp_code=otp_code).exists():
            raise serializers.ValidationError({'otp_code': 'کد وارد شده معتبر نیست یا منقضی شده است.'})
        
        return attrs
    
    def save(self):
        phone_number = self.validated_data['phone_number']
        new_password = self.validated_data['new_password']
        
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'error': 'کاربر یافت نشد.'})

        user.set_password(new_password)
        user.save()

        # حذف تمام OTPهای استفاده‌شده
        OTP.objects.filter(phone_number=phone_number).delete()

        return user



class SendOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate_phone_number(self, value):

        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("شماره موبایل معتبر نیست.")
        return value

    
    
class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp_code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        from .models import OTP
        phone_number = attrs.get("phone_number")
        otp_code = attrs.get("otp_code")

        otp_instance = OTP.objects.filter(phone_number=phone_number, otp_code=otp_code).first()

        if not otp_instance:
            raise serializers.ValidationError({"otp_code": "کد نامعتبر است یا منقضی شده."})

        if otp_instance.is_expired():
            raise serializers.ValidationError({"otp_code": "کد OTP منقضی شده است."})

        return attrs

