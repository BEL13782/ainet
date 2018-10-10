from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', auth_views.logout, {'template_name': 'index.html', 'next_page': '/ainet'}, name='logout'),
    path('reports', views.reports, name='reports'),
    path('cams', views.cams, name='cams'),
    path('zones', views.zones, name='zones'),
    path('add_camera', views.add_camera, name='add_camera'),
    path('add_zone', views.add_zone, name='add_zone'),
    path('add_site', views.add_site, name='add_site'),
    path('update_site/<int:pk>', views.UpdateSite.as_view(), name='update_site'),
    path('update_zone/<int:pk>', views.UpdateZone.as_view(), name='update_zone'),
    path('update_camera/<int:pk>', views.UpdateCamera.as_view(), name='update_camera'),
    path('settings', views.settings, name='settings'),
    path('sites', views.sites, name='sites'),
    path('cams_settings', views.cams, name='cams_settings'),
    path('delete_site/<int:pk>', views.DeleteSite.as_view(), name='delete_site'),
    path('delete_zone/<int:pk>', views.DeleteZone.as_view(), name='delete_zone'),
    path('delete_camera/<int:pk>', views.DeleteCamera.as_view(), name='delete_camera')
]
