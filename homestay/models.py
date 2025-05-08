from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class HomestayFamily(models.Model):
    """
    Represents a homestay family offering accommodations in Dholimara
    """
    name = models.CharField(_('family name'), max_length=100)
    head_of_family = models.CharField(_('head of family'), max_length=100)
    contact_number = models.CharField(_('contact number'), max_length=15)
    email = models.EmailField(_('email'), blank=True, null=True)
    description = models.TextField(_('description'))
    address = models.CharField(_('address'), max_length=255)
    featured_image = models.ImageField(_('featured image'), upload_to='homestay_images/')
    gallery_images = models.ManyToManyField(
        'HomestayImage', 
        related_name='homestay_families', 
        blank=True
    )
    amenities = models.TextField(_('amenities'), blank=True, null=True)
    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('homestay family')
        verbose_name_plural = _('homestay families')
    
    def __str__(self):
        return self.name

class HomestayImage(models.Model):
    """
    Images for homestay families and rooms
    """
    title = models.CharField(_('title'), max_length=100)
    image = models.ImageField(_('image'), upload_to='homestay_images/')
    description = models.TextField(_('description'), blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    def __str__(self):
        return self.title

class Room(models.Model):
    """
    Rooms available in a homestay
    """
    homestay = models.ForeignKey(
        HomestayFamily, 
        on_delete=models.CASCADE, 
        related_name='rooms',
        verbose_name=_('homestay')
    )
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'))
    capacity = models.PositiveSmallIntegerField(_('capacity'))
    price_per_night = models.DecimalField(_('price per night'), max_digits=10, decimal_places=2)
    featured_image = models.ImageField(_('featured image'), upload_to='room_images/')
    gallery_images = models.ManyToManyField(
        HomestayImage, 
        related_name='rooms', 
        blank=True
    )
    amenities = models.TextField(_('amenities'))
    is_available = models.BooleanField(_('is available'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('room')
        verbose_name_plural = _('rooms')
    
    def __str__(self):
        return f"{self.homestay.name} - {self.name}"

class Booking(models.Model):
    """
    Homestay booking information
    """
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('cancelled', _('Cancelled')),
        ('completed', _('Completed')),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='bookings',
        verbose_name=_('user')
    )
    room = models.ForeignKey(
        Room, 
        on_delete=models.CASCADE, 
        related_name='bookings',
        verbose_name=_('room')
    )
    check_in_date = models.DateField(_('check-in date'))
    check_out_date = models.DateField(_('check-out date'))
    number_of_guests = models.PositiveSmallIntegerField(_('number of guests'))
    special_requests = models.TextField(_('special requests'), blank=True, null=True)
    total_price = models.DecimalField(_('total price'), max_digits=10, decimal_places=2)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_date = models.DateTimeField(_('booking date'), auto_now_add=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('booking')
        verbose_name_plural = _('bookings')
    
    def __str__(self):
        return f"Booking {self.id} - {self.user.username} - {self.room.name}"
    
    def save(self, *args, **kwargs):
        # Calculate total price if not already set
        if not self.total_price:
            # Calculate the number of nights
            nights = (self.check_out_date - self.check_in_date).days
            self.total_price = self.room.price_per_night * nights
        super().save(*args, **kwargs)

class Review(models.Model):
    """
    Reviews for homestay experiences
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('user')
    )
    homestay = models.ForeignKey(
        HomestayFamily, 
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('homestay')
    )
    booking = models.OneToOneField(
        Booking, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='review',
        verbose_name=_('booking')
    )
    rating = models.PositiveSmallIntegerField(
        _('rating'),
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(_('comment'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('review')
        verbose_name_plural = _('reviews')
    
    def __str__(self):
        return f"Review by {self.user.username} for {self.homestay.name}"