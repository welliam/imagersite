from django.shortcuts import render


def home_view(request):
    """Return rendered home page."""
    return render(request, 'home.html')
