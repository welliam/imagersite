from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from imager_api.views import photo_api_view

urlpatterns = [
    url('photos/$', photo_api_view, name='photo_api')
]

urlpatterns = format_suffix_patterns(urlpatterns)