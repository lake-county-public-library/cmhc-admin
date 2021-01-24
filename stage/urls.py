from django.urls import path

from . import views

app_name = 'stage'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:status_id>/', views.detail, name='detail'),
    path('<int:status_id>/workflow', views.workflow, name='workflow'),
    path('<int:status_id>/csv', views.stage_csv, name='csv'),
    path('<int:status_id>/images', views.stage_images, name='images'),
    path('<int:status_id>/images_logs', views.images_logs, name='images_logs'),
    path('<int:status_id>/derivatives', views.generate_derivatives, name='derivatives'),
    path('<int:status_id>/logs', views.derivative_logs, name='derivative_logs'),
    path('<int:status_id>/pages', views.generate_pages, name='pages'),
    path('<int:status_id>/pages_logs', views.pages_logs, name='pages_logs'),
    path('<int:status_id>/index', views.generate_index, name='index'),
    path('<int:status_id>/index_logs', views.index_logs, name='index_logs'),
    path('<int:status_id>/run', views.run_local_site, name='run'),
    path('<int:status_id>/run_logs', views.run_local_logs, name='run_logs'),
    path('<int:status_id>/kill', views.kill_local_site, name='kill'),
    path('<int:status_id>/deploy', views.deploy, name='deploy'),
    path('<int:status_id>/deploy_logs', views.deploy_logs, name='deploy_logs'),
]
