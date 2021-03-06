from django.conf.urls import url

from stuff.api import (StuffListCreateAPIView, StuffUpdateAPIView, StuffDestroyAPIView)

urlpatterns = [
    # API
    url(r'^$', StuffListCreateAPIView.as_view(), name='stuff_list_create_api'),
    url(r'^(?P<pk>[0-9A-Za-z_\-]+)/delete/$', StuffDestroyAPIView.as_view(), name='stuff_delete'),
    url(r'^(?P<pk>[0-9A-Za-z_\-]+)/$', StuffUpdateAPIView.as_view(), name='stuff_update_api'),
]
