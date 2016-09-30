from django.shortcuts import render
from django.views.generic.edit import FormView
from django import forms
from .models import Album, Photo
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from django.views.generic import CreateView

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

class UserCreateView(CreateView):
    """View which attaches the request's user to the form being submitted."""

    def form_valid(self, form):
        """Attach the user to the form."""
        form.instance.user = self.request.user
        return super(UserCreateView, self).form_valid(form)


class AddAlbumView(UserCreateView):
    """Add Album View for adding albums."""
    template_name = "add_album.html"
    model = Album
    fields = [
        'title',
        'description',
        'published',
    ]

    @property
    def success_url(self):
        return reverse('library')


class AddPhotoView(UserCreateView):
    """Test Add Photo View for adding photos."""
    template_name = "add_photo.html"
    model = Photo
    fields = [
        'title',
        'description',
        'published',
        'photo'
    ]

    @property
    def success_url(self):
        return reverse('library')
