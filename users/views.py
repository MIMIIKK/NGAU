from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'put', 'patch']
    
    def get_queryset(self):
        # Regular users can only see their own profile
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
