from django import forms
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404

from .models import Album, Photo


def library_view(request):
    """Render a library."""
    photos = request.user.photos.all()
    albums = request.user.albums.all()
    pag_photos = Paginator(photos, 4)
    pag_albums = Paginator(albums, 4)
    page = request.GET.get('page')

    try:
        photos = pag_photos.page(page)
        albums = pag_albums.page(page)
    except PageNotAnInteger:
        albums = pag_albums.page(1)
        photos = pag_photos.page(1)
    except EmptyPage:
        albums = pag_albums.page(pag_albums.num_pages)
        photos = pag_photos.page(pag_photos.num_pages)
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
    if album:
        photos = album.photos.all()
        pag_photos = Paginator(photos, 4)
        page = request.GET.get('page')
        try:
            photos = pag_photos.page(page)
        except PageNotAnInteger:
            photos = pag_photos.page(1)
        except EmptyPage:
            photos = pag_photos.page(pag_photos.num_pages)
        return render(request, 'album.html', dict(album=album, photos=photos))
    else:
        return render(request, 'album_not_found.html')


class UserCreateView(LoginRequiredMixin, CreateView):
    """View which attaches the request's user to the form being submitted."""

    success_url = reverse_lazy('library')

    def form_valid(self, form):
        """Attach the user to the form."""
        form.instance.user = self.request.user
        return super(UserCreateView, self).form_valid(form)


class EditAlbumForm(forms.ModelForm):
    """Form for editing albums.

    Ensures one can only add photos from their own album."""

    class Meta(object):
        model = Album

        fields = [
            'title',
            'description',
            'published',
            'photos',
            'cover'
        ]

    def __init__(self, *args, **kwargs):
        """Limit the photo field's queryset to just photos from this user."""
        user = kwargs.pop('user')
        super(EditAlbumForm, self).__init__(*args, **kwargs)
        queryset = Photo.objects.filter(user=user)
        self.fields['photos'].queryset = queryset
        self.fields['cover'].queryset = queryset

    def clean(self):
        """Ensure an album's cover is in its photos."""
        cleaned_data = super(EditAlbumForm, self).clean()
        cover = cleaned_data.get('cover')
        if cover and cover not in cleaned_data.get('photos'):
            error = forms.ValidationError("Cover not in album's photos.")
            self.add_error('cover', error)


class AddAlbumView(UserCreateView):
    """Add Album View for adding albums."""
    template_name = "add_album.html"
    model = Album
    form_class = EditAlbumForm

    def get_form_kwargs(self):
        kwargs = super(AddAlbumView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class EditAlbumView(UpdateView):
    """View for editing albums."""
    template_name = "edit_album.html"
    model = Album
    success_url = reverse_lazy('library')
    form_class = EditAlbumForm

    def get_form_kwargs(self):
        kwargs = super(EditAlbumView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class DeleteAlbumView(DeleteView):
    """View for deleting albums."""
    template_name = "confirm_delete_album.html"
    model = Album
    success_url = reverse_lazy('library')

    def get_object(self, queryset=None):
        album = super(DeleteAlbumView, self).get_object()
        if album.user != self.request.user:
            raise Http404
        return album


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


class EditPhotoView(UpdateView):
    """View for modifying photo information."""
    template_name = "edit_photo.html"
    model = Photo
    fields = [
        'title',
        'description',
        'published'
    ]
    success_url = reverse_lazy('library')


class DeletePhotoView(DeleteView):
    """View for deleting photos."""
    template_name = "confirm_delete_photo.html"
    model = Photo
    success_url = reverse_lazy('library')

    def get_object(self, queryset=None):
        photo = super(DeletePhotoView, self).get_object()
        if photo.user != self.request.user:
            raise Http404
        return photo
