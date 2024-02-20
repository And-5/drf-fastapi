from rest_framework import serializers

from .models import User, ProfilePhoto, Profile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password')


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_rep = serializers.CharField(required=True)


class ClientPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePhoto
        fields = ['id', 'image']


class ClientProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(source='user.email', read_only=True)
    registration_date = serializers.DateField(read_only=True)
    user_photo = ClientPhotoSerializer(many=True, read_only=True, source='client_photo')

    class Meta:
        model = Profile
        fields = ['id', 'user', 'user_photo', 'registration_date', 'username',
                  'date_of_birth', 'phone']
