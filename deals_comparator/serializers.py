from rest_framework import serializers
from .models import Components

class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Components
        fields = ['vendor','name', 'description', 'price', 'image_url', 'available']