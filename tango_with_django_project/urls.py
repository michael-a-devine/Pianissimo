"""tango_with_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include

from django.core.urlresolvers import reverse
from rango import views
from django.conf import settings
from django.conf.urls.static import static

from registration.backends.simple.views import RegistrationView
from django.contrib.auth.views import password_change, password_change_done


# Create a new class that redirects the user to the index page,
#if successful at logging
class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
       # return '/pianissimo/'
        return reverse('register_profile')

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'index/$', views.index, name='index'),
    url(r'^pianissimo/', include('rango.urls')),
    url(r'rango/$', views.index, name='index'),
    # above maps any URLs starting with rango/ to be handled by the rango application
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^accounts/password/change/$', password_change, {'template_name': 'registration/password_change_form.html'}, name='password_change'),
    url(r'^accounts/password/change/done/$', password_change_done, {'template_name': 'registration/password_change_done.html'}, name='password_change_done'),
  #  url(r'^accounts/password/change/$', MyRegistrationView.as_view(), name="auth_password_change"),
  # url(r'^accounts/password/change/done/$', MyRegistrationView.as_view(), name="auth_password_changed"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
