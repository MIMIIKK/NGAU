from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, CulturalEvent, FoodItem, LifestyleElement, OkBajiStory, Gallery, Testimonial
from .serializers import (
    CategorySerializer, CulturalEventSerializer, FoodItemSerializer,
    LifestyleElementSerializer, OkBajiStorySerializer, GallerySerializer, TestimonialSerializer
)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class CulturalEventViewSet(viewsets.ModelViewSet):
    queryset = CulturalEvent.objects.all().order_by('-created_at')
    serializer_class = CulturalEventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'is_featured']
    search_fields = ['title', 'description']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all().order_by('-created_at')
    serializer_class = FoodItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_vegetarian', 'is_featured']
    search_fields = ['name', 'description', 'ingredients']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

class LifestyleElementViewSet(viewsets.ModelViewSet):
    queryset = LifestyleElement.objects.all().order_by('-created_at')
    serializer_class = LifestyleElementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_featured']
    search_fields = ['title', 'description']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

class OkBajiStoryViewSet(viewsets.ModelViewSet):
    queryset = OkBajiStory.objects.all().order_by('-year')
    serializer_class = OkBajiStorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'story']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all().order_by('-created_at')
    serializer_class = GallerySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'is_featured']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all().order_by('-created_at')
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_featured']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()