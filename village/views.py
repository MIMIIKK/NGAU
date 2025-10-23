from rest_framework import viewsets, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Category, CulturalEvent, FoodItem, LifestyleElement,
    OkBajiStory, Gallery, Testimonial, HighlightItem
)
from .serializers import (
    CategorySerializer, CulturalEventSerializer, FoodItemSerializer,
    LifestyleElementSerializer, OkBajiStorySerializer, GallerySerializer,
    TestimonialSerializer, HighlightItemSerializer
)


# ------------------- ViewSets -------------------

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
    """
    API endpoint for testimonials.
    Users can view and post testimonials for specific items.
    """
    queryset = Testimonial.objects.all().order_by('-created_at')
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.AllowAny]  # anyone can view or post
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['section', 'item_id']  # filter by section and specific item
    search_fields = ['name', 'country', 'message']

    def get_permissions(self):
        """
        Allow anyone to view and create testimonials.
        Only admin can update or delete.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()


# ------------------- Highlight API -------------------

class HighlightListAPIView(APIView):
    """
    API endpoint to fetch all featured highlight items for homepage.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # Only featured items, newest first
        items = HighlightItem.objects.filter(featured=True).order_by('-created_at')
        serializer = HighlightItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
