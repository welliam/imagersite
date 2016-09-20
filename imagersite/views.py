from django.shortcuts import render
from django.http import HttpResponse


def home_view(request):
    """Return rendered home page."""
    return render(request, 'home.html', context={})
