# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import include, url

from simpl_users.apis.urls import router as api_router


# Our application urls
urlpatterns = [
    url(r'^apis/', include(api_router.urls, namespace='simpl_users_api')),
    url(r'^users/', include('simpl_users.urls', namespace='users')),
]
