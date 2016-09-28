from django.shortcuts import render


def library_view(request):
    """Render a library."""
    photos = request.user.photos.all()
    return render(request, 'library.html', dict(photos=photos))


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
    return render(request, 'album.html', dict(album=album))
