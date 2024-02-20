from django.contrib.auth import update_session_auth_hash
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from .serializers import *


class UserRegistrationView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user = User.objects.filter(email=data["email"]).first()
        if user:
            return Response({'error': 'User already exist'}, status=409)

        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response_data = {
            'id': user.id,
            'email': user.email,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }
        return Response(response_data, status=201)


class UserLoginView(APIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None:
            return Response({'error': 'Please provide email'}, status=400)
        if password is None:
            return Response({'error': 'Please provide password'}, status=400)

        user = User.objects.filter(email=email).first()
        if user is None:
            return Response({'error': 'Invalid email'}, status=400)
        if not user.check_password(password):
            return Response({'error': 'Invalid password'}, status=400)

        refresh = RefreshToken.for_user(user)
        response_data = {
            'id': user.id,
            'email': user.email,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }
        return Response(response_data, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.data.get('old_password')
            if user.check_password(old_password):
                new_password = serializer.data.get('new_password')
                new_password_rep = serializer.data.get('new_password_rep')

                if old_password == new_password:
                    return Response({'error': 'The new password must be obtained from the old one.'},
                                    status=status.HTTP_400_BAD_REQUEST)
                if new_password == new_password_rep:
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)  # To update session after password change
                    return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'New passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ClientProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_object(self):
        user = self.request.user
        return Profile.objects.filter(user=user).first()


class ProfilePhotoListCreateView(generics.ListCreateAPIView):
    queryset = ProfilePhoto.objects.all()
    serializer_class = ClientPhotoSerializer

    def perform_create(self, serializer):
        user_profile = Profile.objects.get(user=self.request.user)
        serializer.save(user=user_profile)


class ProfilePhotoRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = ProfilePhoto.objects.all()
    serializer_class = ClientPhotoSerializer

    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if self.request.user == instance.user.user:
            try:
                photo = instance.image
                photo.delete()
                instance.delete()
            except Exception as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied("You do not have permission to delete this photo.")
