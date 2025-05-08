from django.contrib import admin
from .models import Category, CulturalEvent, FoodItem, LifestyleElement, OkBajiStory, Gallery, Testimonial

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

@admin.register(CulturalEvent)
class CulturalEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_vegetarian', 'is_featured', 'created_at')
    list_filter = ('is_vegetarian', 'is_featured')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description', 'ingredients')

@admin.register(LifestyleElement)
class LifestyleElementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_featured', 'created_at')
    list_filter = ('is_featured',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')

@admin.register(OkBajiStory)
class OkBajiStoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'year')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'story')

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'description', 'location')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'is_featured', 'created_at')
    list_filter = ('country', 'is_featured')
    search_fields = ('name', 'message', 'country')