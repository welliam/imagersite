from rest_framework import serializers
from image.models import Photo

class PhotoSerializer(serializers.ModelSerializer):
    """Photo serializer."""

    class Meta:
        model=Photo
        fields = (
            'title', 
            'description', 
            'date_uploaded',
            'date_modified',
            'date_published',
            'published',
        )