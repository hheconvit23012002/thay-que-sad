from rest_framework import serializers
from .models import *

class ShipDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipDetail
        fields = "__all__"

class ShipSerializer(serializers.ModelSerializer):
    details = ShipDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Ship
        fields = "__all__"
