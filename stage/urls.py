from django.urls import path

from . import views

app_name = 'stage'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:status_id>/', views.detail, name='detail'),
    path('<int:status_id>/workflow', views.workflow, name='workflow'),
    path('<int:status_id>/csv', views.stage_csv, name='csv'),
    path('<int:status_id>/images', views.stage_images, name='images'),
    path('<int:status_id>/derivatives', views.generate_derivatives, name='derivatives'),
    path('<int:status_id>/logs', views.derivative_logs, name='derivative_logs'),
    path('<int:status_id>/rebuild', views.rebuild_local_site, name='rebuild'),
    path('<int:status_id>/run', views.run_local_site, name='run'),
    path('<int:status_id>/deploy', views.deploy, name='deploy'),
]
