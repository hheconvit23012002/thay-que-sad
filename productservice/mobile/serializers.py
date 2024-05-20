from rest_framework import serializers
from .models import *
from book.serializers import *

class MobileSerializer(serializers.ModelSerializer):
    productDetail = ProductSerializer(source='product', read_only=True)
    categoryDetail = CategorySerializer(source='category',read_only=True)
    class Meta:
        model = Mobile
        fields = '__all__'

    # def get_productDetail(self, obj):
    #     items = obj.product_set.first()
    #     serializer = ProductSerializer(items, many=True)
    #     return serializer.data