from django.shortcuts import render


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
        'request': request
    })

