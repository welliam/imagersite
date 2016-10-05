from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from imager_api.serializer import PhotoSerializer
from image.models import Photo
from django.contrib.auth.decorators import login_required


@login_required
@api_view(['GET'])
def photo_api_view(request, format=None):
    """Get photo api"""
    photos = Photo.objects.filter(user=request.user)
    serializer = PhotoSerializer(photos, many=True)
    return Response(serializer.data)
