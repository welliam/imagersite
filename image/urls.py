from .views import library_view
from django.conf.urls import url

urlpatterns = [
    url('^library$', library_view, name='library')
]
