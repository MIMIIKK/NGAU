from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, CulturalEventViewSet, FoodItemViewSet,
    LifestyleElementViewSet, OkBajiStoryViewSet, GalleryViewSet, TestimonialViewSet
)

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('cultural-events', CulturalEventViewSet)
router.register('food-items', FoodItemViewSet)
router.register('lifestyle', LifestyleElementViewSet)
router.register('ok-baji', OkBajiStoryViewSet)
router.register('gallery', GalleryViewSet)
router.register('testimonials', TestimonialViewSet)

urlpatterns = [
    path('', include(router.urls)),
]