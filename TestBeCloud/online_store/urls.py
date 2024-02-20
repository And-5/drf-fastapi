from rest_framework.routers import DefaultRouter
from django.urls import path, include
from online_store.views import one_product_from_another_service, all_product_from_another_service, \
    create_product, delete_product, update_product

app_name = 'store'

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('create_product/', create_product),
    path('delete_product/', delete_product),
    path('update_product/<int:product_id>/', update_product),
    path('all_product/', all_product_from_another_service),
    path('one_product/', one_product_from_another_service),
]
