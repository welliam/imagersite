from django.shortcuts import render


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
