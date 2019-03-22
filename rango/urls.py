

from django.conf.urls import url
from rango import views




urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_piece/$', views.add_piece, name='add_piece'),
    url(r'music/$', views.music, name='music'),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
    #url(r'piece/$', views.piece, name='piece'),
    url(r'^piece/(?P<piece_title_slug>[\w\-]+)/$', views.piece, name='piece'),
]
