from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from custom_auth.views import *

app_name = 'custom_auth'

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('registration/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('refresh-token/', TokenRefreshView.as_view(), name='token-refresh'),
    path('change_password/', change_password, name='change_password'),
    path('profile/<int:pk>/', ClientProfileView.as_view()),
    path('profile/photo/', ProfilePhotoListCreateView.as_view()),
    path('profile/photo/delete/<int:pk>/', ProfilePhotoRetrieveDestroyView.as_view()),
]
