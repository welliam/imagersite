from .views import library_view, image_view, album_view, AddAlbumView
from django.conf.urls import url

urlpatterns = [
    url('library/$', library_view, name='library'),
    url(r'photos/(?P<photo_id>[0-9]+)/$', image_view, name='images'),
    url(r'album/(?P<album_id>[0-9]+)/$', album_view, name='album'),
    url(r'album/add', AddAlbumView.as_view(), name='add_album'),
]
