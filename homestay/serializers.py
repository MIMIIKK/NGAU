from rest_framework import serializers
from .models import HomestayFamily, HomestayImage, Room, Booking, Review


class HomestayImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = HomestayImage
        fields = '__all__'

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class RoomSerializer(serializers.ModelSerializer):
    featured_image = serializers.SerializerMethodField()
    gallery_images = HomestayImageSerializer(many=True, read_only=True)
    homestay_name = serializers.CharField(source="homestay.name", read_only=True)

    class Meta:
        model = Room
        fields = '__all__'

    def get_featured_image(self, obj):
        request = self.context.get("request")
        if obj.featured_image and hasattr(obj.featured_image, "url"):
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            return obj.featured_image.url
        return None


class HomestayFamilySerializer(serializers.ModelSerializer):
    featured_image = serializers.SerializerMethodField()
    rooms = RoomSerializer(many=True, read_only=True)
    gallery_images = HomestayImageSerializer(many=True, read_only=True)

    class Meta:
        model = HomestayFamily
        fields = '__all__'

    def get_featured_image(self, obj):
        request = self.context.get("request")
        if obj.featured_image and hasattr(obj.featured_image, "url"):
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            return obj.featured_image.url
        return None


class BookingSerializer(serializers.ModelSerializer):
    homestay_name = serializers.CharField(source="room.homestay.name", read_only=True)
    room_name = serializers.CharField(source="room.name", read_only=True)
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['total_price', 'status', 'booking_date']

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username

    def validate(self, data):
        if data['check_out_date'] <= data['check_in_date']:
            raise serializers.ValidationError({"check_out_date": "Check out date must be after check in date."})

        overlapping_bookings = Booking.objects.filter(
            room=data['room'],
            status__in=['pending', 'confirmed'],
            check_in_date__lt=data['check_out_date'],
            check_out_date__gt=data['check_in_date']
        )

        if overlapping_bookings.exists():
            raise serializers.ValidationError({"room": "This room is not available for the selected dates."})

        return data


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    homestay_name = serializers.CharField(source="homestay.name", read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user']

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username
