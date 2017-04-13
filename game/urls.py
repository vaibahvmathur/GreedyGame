from django.conf.urls import url
from game.views import *


urlpatterns = [
    url(r'^$', HomePage, name='Homepage'),
]