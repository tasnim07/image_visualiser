
from django.conf.urls import include, url

from rest_framework import routers

from visualiser import api

router = routers.SimpleRouter()

router.register(r'image', api.ImageView, 'image')

urlpatterns = [
    # API Methods
    url(r'^', include(router.urls)),
]
