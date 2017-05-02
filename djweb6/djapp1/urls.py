from django.conf.urls import url

from . import views

app_name = 'djapp1'

urlpatterns = [
    url(r'^$', views.homepage,
        name='homepage'),
]
