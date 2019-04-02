from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'jobindex/(?P<pIndex>[0-9]+)$', views.index, name="index"),
]