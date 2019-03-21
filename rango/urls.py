

from django.conf.urls import url
from rango import views


### When there are more than one app:

#app_name = 'rango'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_piece/$', views.add_piece, name='add_piece'),    
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'search/$', views.search, name='search'),
    url(r'music/$', views.music, name='music'),
]
