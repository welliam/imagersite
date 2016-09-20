from django.shortcuts import render


def home_view(request):
    """Return rendered home page."""
    return render(request, 'home.html', context={})


def register_view(request):
    """Return rendered register page."""
    return render(request, 'register.html', context={})
