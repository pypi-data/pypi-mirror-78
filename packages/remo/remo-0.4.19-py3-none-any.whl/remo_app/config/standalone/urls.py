from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

from remo_app.remo.api.views.local_files import LocalFiles
from remo_app.remo.api.views.medial_files import MediaFiles
from remo_app.remo.api.views.settings import Settings
from remo_app.remo.api.views.version import Version

urlpatterns = [
    url(r'^settings/?$', csrf_exempt(Settings.as_view()), name='settings'),
    url(r'^version/?$', csrf_exempt(Version.as_view()), name='version'),
    url(r'^api/', include('remo_app.remo.api.urls')),
    url(r'^api/v1/ui/', include('remo_app.remo.api.v1.ui.urls')),
    url(r'^api/v1/sdk/', include('remo_app.remo.api.v1.sdk.urls')),
    url(r'^docs/', include('remo_app.remo.docs.urls')),
]

urlpatterns += [
    url(r'^%s/.*$' % settings.LOCAL_FILES.lstrip('/'), csrf_exempt(LocalFiles.as_view()), name='local-files'),
    url(r'^%s.*$' % settings.MEDIA_URL.lstrip('/'), csrf_exempt(MediaFiles.as_view()), name='media-files'),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]
