from django.shortcuts import render
from image.models import Photo
from django.conf import settings

def home_view(request):
    """Return rendered home page."""
    random_photo = Photo.objects.order_by("?").first()
    if random_photo:
        random_photo = random_photo.url
    else:
        random_photo = settings.STATIC_URL + 'bird.jpg'
    return render(request, 'home.html', context={"random_image_url": random_photo})
