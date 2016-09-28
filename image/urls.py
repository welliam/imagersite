from .views import library_view, image_view
from django.conf.urls import url

urlpatterns = [
    url('library/$', library_view, name='library'),
    url(r'photos/(?P<photo_id>[0-9]+)/$', image_view, name='images')
]
