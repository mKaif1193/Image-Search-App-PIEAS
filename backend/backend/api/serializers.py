from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    name = serializers.CharField(required=False, allow_blank=True)
    caption = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Image
        fields = ("id", "name", "caption", "image", "category", "created_at")
