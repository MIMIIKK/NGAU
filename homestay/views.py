from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
from django.db.models import Avg, Count

from .models import HomestayFamily, HomestayImage, Room, Booking, Review
from .serializers import HomestayFamilySerializer, HomestayImageSerializer, RoomSerializer, BookingSerializer, ReviewSerializer

class HomestayFamilyViewSet(viewsets.ModelViewSet):
    queryset = HomestayFamily.objects.filter(is_active=True)
    serializer_class = HomestayFamilySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description', 'address']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured homestay families with room count and average rating"""
        homestays = HomestayFamily.objects.filter(is_active=True)
        homestays = homestays.annotate(
            room_count=Count('rooms'),
            avg_rating=Avg('reviews__rating')
        ).order_by('-avg_rating')[:5]
        serializer = self.get_serializer(homestays, many=True)
        return Response(serializer.data)

class HomestayImageViewSet(viewsets.ModelViewSet):
    queryset = HomestayImage.objects.all()
    serializer_class = HomestayImageSerializer
    permission_classes = [permissions.IsAdminUser]

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.filter(is_available=True)
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['homestay', 'capacity', 'is_available']
    search_fields = ['name', 'description', 'amenities']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()
    
    @action(detail=False, methods=['post'])
    def check_availability(self, request):
        """Check room availability for specific dates"""
        try:
            check_in = request.data.get('check_in_date')
            check_out = request.data.get('check_out_date')
            
            if not check_in or not check_out:
                return Response(
                    {"error": "Please provide both check_in_date and check_out_date"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
            
            # Validate dates
            if check_out_date <= check_in_date:
                return Response(
                    {"error": "Check-out date must be after check-in date"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get all rooms
            rooms = Room.objects.filter(is_available=True)
            
            # Filter out rooms with overlapping bookings
            available_rooms = []
            for room in rooms:
                overlapping_bookings = Booking.objects.filter(
                    room=room,
                    status__in=['pending', 'confirmed'],
                    check_in_date__lt=check_out_date,
                    check_out_date__gt=check_in_date
                )
                
                if not overlapping_bookings.exists():
                    available_rooms.append(room)
            
            # Optional: filter by capacity if provided
            capacity = request.data.get('capacity')
            if capacity:
                available_rooms = [r for r in available_rooms if r.capacity >= int(capacity)]
            
            serializer = self.get_serializer(available_rooms, many=True)
            return Response(serializer.data)
            
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST
            )

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'room', 'check_in_date', 'check_out_date']
    
    def get_queryset(self):
        # Regular users can only see their own bookings
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking"""
        booking = self.get_object()
        
        # Check if the booking can be cancelled
        if booking.status not in ['pending', 'confirmed']:
            return Response(
                {"error": "Only pending or confirmed bookings can be cancelled"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'cancelled'
        booking.save()
        
        serializer = self.get_serializer(booking)
        return Response(serializer.data)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['homestay', 'rating']
    
    def get_queryset(self):
        return Review.objects.all().order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
