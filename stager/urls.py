from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.dashboard, name='dashboard'),
        url(r'^add_repository/$', views.add_repository, name='add_repository'),
        url(r'^webhooks/(?P<user_id>\w+)/(?P<project_id>\w+)/$', views.webhooks, name='webhooks'),
]
