from django.views.generic import UpdateView
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import UserProfile


def profile_view(request):
    """Return rendered profile page."""
    return render(request, 'profile.html', context={
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'camera_type': request.user.profile.camera_type,
        'genre': request.user.profile.genre,
        'is_professional': request.user.profile.is_professional,
        'hireable': request.user.profile.hireable,
        'request': request,
        'photos_uploaded': len(request.user.photos.all()),
        'albums_created': len(request.user.albums.all()),
    })


class EditProfileView(UpdateView):
    """View for editing profiles."""
    template_name = "edit_profile.html"
    model = UserProfile
    fields = [
        'camera_type',
        'genre',
        'is_professional',
        'hireable',
        'website',
    ]
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile
