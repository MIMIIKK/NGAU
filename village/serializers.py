from rest_framework import serializers
from .models import Category, CulturalEvent, FoodItem, LifestyleElement, OkBajiStory, Gallery, Testimonial

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CulturalEventSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = CulturalEvent
        fields = '__all__'

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = '__all__'

class LifestyleElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifestyleElement
        fields = '__all__'

class OkBajiStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OkBajiStory
        fields = '__all__'

class GallerySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Gallery
        fields = '__all__'

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'