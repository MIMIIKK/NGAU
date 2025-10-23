from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # Use ImageField for both read and write operations
    profile_image = serializers.ImageField(required=False, allow_null=True)
    # Add a separate field for the URL
    profile_image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'profile_image',
            'profile_image_url',
            'bio',
        )
        read_only_fields = ('id', 'email')
        extra_kwargs = {
            'profile_image': {'write_only': True}  # Only for uploads
        }

    def get_profile_image_url(self, obj):
        """Return absolute URL for profile image"""
        request = self.context.get('request')
        if obj.profile_image:
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
            return obj.profile_image.url
        return None

    def update(self, instance, validated_data):
        """Handle profile image updates"""
        # If a new profile_image is provided, the old one will be replaced
        profile_image = validated_data.get('profile_image', None)
        
        if profile_image is not None:
            # Delete old image if it exists
            if instance.profile_image:
                instance.profile_image.delete(save=False)
            instance.profile_image = profile_image
        
        # Update other fields
        for attr, value in validated_data.items():
            if attr != 'profile_image':
                setattr(instance, attr, value)
        
        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user