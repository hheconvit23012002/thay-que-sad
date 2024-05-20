from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    info = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = '__all__'

    def get_info(self, obj):
        context = self.context
        info_data = context.get("info")
        return info_data


class BookSerializer(serializers.ModelSerializer):
    productDetail = ProductSerializer(source='product', read_only=True)
    categoryDetail = CategorySerializer(source='category',read_only=True)
    class Meta:
        model = Book
        fields = '__all__'

