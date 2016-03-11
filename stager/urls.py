from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^login/$', views.login, name='login'),
        url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/stager/login/'}, name='logout'),
        url(r'^', views.dashboard, name='dashboard'),
        url(r'^add_repository/$', views.add_repository, name='add_repository'),
        url(r'^create_webhook/(?P<project_uuid>\w+)/$', views.create_webhook, name='create_webhook'),
        url(r'^webhooks/(?P<user_id>\w+)/(?P<project_id>\w+)/$', views.webhooks, name='webhooks'),
]
