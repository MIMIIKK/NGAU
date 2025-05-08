from django.contrib import admin
from .models import HomestayFamily, HomestayImage, Room, Booking, Review

class RoomInline(admin.TabularInline):
    model = Room
    extra = 0

@admin.register(HomestayFamily)
class HomestayFamilyAdmin(admin.ModelAdmin):
    list_display = ('name', 'head_of_family', 'contact_number', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'address', 'description')
    inlines = [RoomInline]

@admin.register(HomestayImage)
class HomestayImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'homestay', 'capacity', 'price_per_night', 'is_available')
    list_filter = ('is_available', 'homestay')
    search_fields = ('name', 'description', 'amenities')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'check_in_date', 'check_out_date', 'number_of_guests', 'status', 'total_price')
    list_filter = ('status', 'check_in_date', 'check_out_date')
    search_fields = ('user__username', 'user__email', 'room__name', 'special_requests')
    readonly_fields = ('booking_date', 'created_at', 'updated_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'homestay', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'homestay__name', 'comment')
    readonly_fields = ('created_at', 'updated_at')

