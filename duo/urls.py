from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.rd),
    url(r'^xp/$', views.xp, name="xp"),
    url(r'^streak/$', views.streak, name="streak"),
    url(r'^lingots/$', views.lingots, name="lingots"),
    url(r'^about/$', views.about, name="about"),
    url(r'^submit/$', views.submit, name="submit"),
    #url(r'^submit/username/$', views.submit_user, name="submit_user")
]
