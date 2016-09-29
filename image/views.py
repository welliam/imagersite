from django.shortcuts import render
from django.views.generic.edit import FormView
from django import forms
from .models import Album
from django.urls import reverse
from django.http.response import HttpResponseRedirect

def library_view(request):
    """Render a library."""
    photos = request.user.photos.all()
    albums = request.user.albums.all()
    for album in albums:
        if not album.cover:
            album.nocover = True
    context = dict(photos=photos, albums=albums)
    return render(request, 'library.html', context)


def image_view(request, photo_id):
    """Render an image."""
    photo = request.user.photos.filter(id=photo_id).first()
    if photo:
        return render(request, 'photo.html', dict(photo=photo))
    else:
        return render(request, 'photo_not_found.html')


def album_view(request, album_id):
    """Render detail view of album."""
    album = request.user.albums.filter(id=album_id).first()
    photos = album.photos.all()
    return render(request, 'album.html', dict(album=album, photos=photos))



class AddAlbumForm(forms.ModelForm):
    """Add Albumb Form"""
    class  Meta(object):
        model = Album
        fields = [
            'title',
            'description',
            'published',
        ]

class AddAlbumView(FormView):
    """Add Album View for adding albums."""
    template_name = "add_album.html"
    form_class = AddAlbumForm

    def form_valid(self, form):
        return HttpResponseRedirect(reverse('library'))
    #Django is weird. Not as prop fails.
    @property
    def success_url(self):
        return reverse('library')