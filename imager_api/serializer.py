from rest_framework import serializers
from image.models import Photo

class PhotoSerializer(serializers.ModelSerializer):
    """Photo serializer."""

    class Meta:
        model=Photo
