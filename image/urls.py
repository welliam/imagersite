from .views import (
    library_view,
    image_view,
    album_view,
    AddAlbumView,
    AddPhotoView,
    EditPhotoView,
    EditAlbumView
)
from django.conf.urls import url

urlpatterns = [
    url('library/$', library_view, name='library'),

    url(r'photos/add', AddPhotoView.as_view(), name='add_photo'),
    url(r'photos/(?P<photo_id>[0-9]+)/$', image_view, name='images'),
    url(
        r'photos/(?P<pk>[0-9]+)/edit/$',
        EditPhotoView.as_view(),
        name='edit_photo'
    ),

    url(r'album/add', AddAlbumView.as_view(), name='add_album'),
    url(r'album/(?P<album_id>[0-9]+)/$', album_view, name='album'),
    url(
        r'album/(?P<pk>[0-9]+)/edit/$',
        EditAlbumView.as_view(),
        name='edit_album'
    ),
]
