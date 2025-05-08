from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    """
    Categories for content (culture, traditions, food, lifestyle)
    """
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
    
    def __str__(self):
        return self.name

class CulturalEvent(models.Model):
    """
    Cultural events and traditions
    """
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), unique=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        related_name='cultural_events',
        verbose_name=_('category')
    )
    description = models.TextField(_('description'))
    featured_image = models.ImageField(_('featured image'), upload_to='cultural_images/')
    importance = models.TextField(_('importance'), blank=True, null=True)
    season = models.CharField(_('season'), max_length=100, blank=True, null=True)
    video_url = models.URLField(_('video URL'), blank=True, null=True)
    is_featured = models.BooleanField(_('is featured'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('cultural event')
        verbose_name_plural = _('cultural events')
    
    def __str__(self):
        return self.title

class FoodItem(models.Model):
    """
    Traditional food items
    """
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'))
    ingredients = models.TextField(_('ingredients'))
    preparation = models.TextField(_('preparation method'))
    featured_image = models.ImageField(_('featured image'), upload_to='food_images/')
    cultural_significance = models.TextField(_('cultural significance'), blank=True, null=True)
    is_vegetarian = models.BooleanField(_('is vegetarian'), default=False)
    is_featured = models.BooleanField(_('is featured'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('food item')
        verbose_name_plural = _('food items')
    
    def __str__(self):
        return self.name

class LifestyleElement(models.Model):
    """
    Elements of daily lifestyle in Dholimara
    """
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'))
    featured_image = models.ImageField(_('featured image'), upload_to='lifestyle_images/')
    is_featured = models.BooleanField(_('is featured'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('lifestyle element')
        verbose_name_plural = _('lifestyle elements')
    
    def __str__(self):
        return self.title

class OkBajiStory(models.Model):
    """
    Stories about OK Baji (Kazumasa Kakimi)
    """
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), unique=True)
    year = models.PositiveIntegerField(_('year'), blank=True, null=True)
    story = models.TextField(_('story'))
    impact = models.TextField(_('impact'), blank=True, null=True)
    featured_image = models.ImageField(_('featured image'), upload_to='okbaji_images/')
    is_featured = models.BooleanField(_('is featured'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('OK Baji story')
        verbose_name_plural = _('OK Baji stories')
        ordering = ['-year']
    
    def __str__(self):
        return self.title

class Gallery(models.Model):
    """
    Photo gallery for the village
    """
    title = models.CharField(_('title'), max_length=200)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        related_name='galleries',
        verbose_name=_('category')
    )
    description = models.TextField(_('description'), blank=True, null=True)
    image = models.ImageField(_('image'), upload_to='gallery/')
    location = models.CharField(_('location'), max_length=200, blank=True, null=True)
    date_taken = models.DateField(_('date taken'), blank=True, null=True)
    is_featured = models.BooleanField(_('is featured'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('gallery item')
        verbose_name_plural = _('gallery items')
    
    def __str__(self):
        return self.title

class Testimonial(models.Model):
    """
    Visitor testimonials
    """
    name = models.CharField(_('name'), max_length=100)
    country = models.CharField(_('country'), max_length=100)
    message = models.TextField(_('message'))
    photo = models.ImageField(_('photo'), upload_to='testimonials/', blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    is_featured = models.BooleanField(_('is featured'), default=False)
    
    class Meta:
        verbose_name = _('testimonial')
        verbose_name_plural = _('testimonials')
    
    def __str__(self):
        return f"{self.name} from {self.country}"