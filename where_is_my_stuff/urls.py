# -*- coding: utf-8 -*-
"""Root url routering file.

You should put the url config in their respective app putting only a
refernce to them here.
"""
from __future__ import absolute_import, unicode_literals
import base64

# Third Party Stuff
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as dj_default_views
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from allauth.account.views import PasswordResetFromKeyView
from rest_framework_jwt.views import refresh_jwt_token

# where_is_my_stuff_api Stuff
from base import views as base_views
from base.utils.axes_decorator import watch_login


class PasswordResetFromKeyDecodePKView(PasswordResetFromKeyView):

    # django-allauth requires decoded UUID field if pk is not an integer
    def dispatch(self, request, uidb64, key, **kwargs):
        uuid = base64.urlsafe_b64decode(uidb64)
        return super(PasswordResetFromKeyDecodePKView, self).dispatch(request, uuid, key, **kwargs)


handler500 = base_views.server_error

# Top Level Pages
# ==============================================================================
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name="home"),
    # Your stuff: custom urls go here
]

urlpatterns += [

    url(r'^(?P<filename>(robots.txt)|(humans.txt))$',
        base_views.root_txt_files, name='root-txt-files'),

    # Rest API
    url(r'^api/stuff/', include('stuff.urls_api', namespace='stuff')),

    # Browsable API
    url(r'^api/auth-n/', include('rest_framework.urls', namespace='rest_framework')),

    # Django Admin
    url(r'^admin/', include(admin.site.urls)),

    # django-allauth
    url(r'^accounts/', include('allauth.urls')),

    # Django REST Auth
    url(r'^api/auth/login/$', csrf_exempt(watch_login(base_views.NoCSRFLoginView.as_view())), name='rest_login'),
    url(r'^api/auth/', include('rest_auth.urls')),
    url(r'^api/auth/registration/', include('rest_auth.registration.urls')),
    url(r'^api/auth/token-refresh/', refresh_jwt_token),

    url(r'^password-reset/confirm/([0-9A-Za-z_\-]+)/([0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetFromKeyDecodePKView.as_view(), name='password_reset_confirm'),

    # this url is used only to generate django-rest-auth email content
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        TemplateView.as_view(), name='password_reset_confirm'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^400/$', dj_default_views.bad_request, kwargs={'exception': Exception("Bad Request!")}),
        url(r'^403/$', dj_default_views.permission_denied, kwargs={'exception': Exception("Permission Denied!")}),
        url(r'^404/$', dj_default_views.page_not_found, kwargs={'exception': Exception("Not Found!")}),
        url(r'^500/$', handler500),

        url(r'^docs/', include('rest_framework_docs.urls')),

        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
