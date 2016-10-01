from django.conf.urls import url
from .views import profile_view, EditProfileView


urlpatterns = [
    url(r'^$', profile_view, name='profile'),
    url(r'edit$', EditProfileView.as_view(), name='edit_profile'),
]
