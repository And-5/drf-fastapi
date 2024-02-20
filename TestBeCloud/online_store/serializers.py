from rest_framework import serializers


class ProductIdSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)


class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    price = serializers.IntegerField(required=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if 'price' in representation and representation['price'] is not None:
            representation['price'] = str(representation['price'])
        return representation
