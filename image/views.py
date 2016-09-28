from django.shortcuts import render

# Create your views here.

def library_view(request):
    """Render a library."""
    return render(request, 'library.html', {
        'photos': request.user.photos.all()
    })


def image_view(request, photo_id):
    """Render an image."""
    return render(request, 'library.html', {
        'photos': request.user.photos.all()
    })
