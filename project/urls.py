from django.conf.urls import patterns, url

from project import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^(?P<user_id>\d+)/logout/$', views.logout, name='logout'),
)
