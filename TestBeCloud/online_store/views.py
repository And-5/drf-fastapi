import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from online_store.serializers import ProductIdSerializer, ProductSerializer

URL = "http://127.0.0.1:8001"


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def one_product_from_another_service(request):
    serializer = ProductIdSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    product_id = serializer.validated_data['product_id']
    try:
        url = f'{URL}/store/{product_id}'
        response = requests.get(url)
        print(response)
        response.raise_for_status()
        data = response.json()
        return Response(data)
    except requests.exceptions.RequestException as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_product_from_another_service(request):
    try:
        url = f'{URL}/store'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return Response(data)
    except requests.exceptions.RequestException as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    url = f'{URL}/store'
    serializer = ProductSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    product_json = serializer.data
    response = requests.post(url, json=product_json)

    if response.status_code == 200:
        return Response({"status": "success", "data": response.json()})
    else:
        return Response({"error": "Failed to create product in another service"}, status=500)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request):
    serializer = ProductIdSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    product_id = serializer.validated_data['product_id']
    try:
        url = f'{URL}/store/{product_id}'
        response = requests.delete(url)
        response.raise_for_status()
        data = response.json()
        return Response(data)
    except requests.exceptions.RequestException as e:
        return Response({'error': str(e)}, status=500)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_product(request, product_id):
    url = f'{URL}/store/{product_id}'
    serializer = ProductSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    product_json = serializer.data
    response = requests.patch(url, json=product_json)

    if response.status_code == 200:
        return Response({"status": "success", "data": response.json()})
    else:
        return Response({"error": "Failed to create product in another service"}, status=500)
