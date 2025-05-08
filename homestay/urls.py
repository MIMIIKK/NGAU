from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HomestayFamilyViewSet, HomestayImageViewSet, RoomViewSet, BookingViewSet, ReviewViewSet

router = DefaultRouter()
router.register('families', HomestayFamilyViewSet)
router.register('images', HomestayImageViewSet)
router.register('rooms', RoomViewSet)
router.register('bookings', BookingViewSet, basename='booking')
router.register('reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]

