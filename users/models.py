from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """
    Custom User model with additional fields
    """
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(_('phone number'), max_length=15, blank=True, null=True)
    profile_image = models.ImageField(_('profile image'), upload_to='profile_images/', blank=True, null=True)
    bio = models.TextField(_('bio'), blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email