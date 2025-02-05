from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username"]

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  \
        blank=True
    )

    def __str__(self):
        return self.phone_number


class OTP(models.Model):
    phone_number = models.CharField(max_length=15)  
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self, validity_period=30):

        return (timezone.now() - self.created_at).seconds < validity_period  

    def __str__(self):
        return f"{self.phone_number} - {self.otp_code}"
