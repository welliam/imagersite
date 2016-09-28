from django.shortcuts import render
from django.urls import reverse


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
