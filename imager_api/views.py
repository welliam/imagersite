from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def photo_api_view(request, format=None):
    """Get photo api"""
    return Response({})
