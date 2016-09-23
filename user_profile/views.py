from django.shortcuts import render


def profile_view(request):
    """Return rendered profile page."""
    import pdb; pdb.set_trace
    return render(request, 'profile.html', context={
    })

