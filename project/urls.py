from django.conf.urls import patterns, url

from project import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^(?P<user_id>\d+)/logout/$', views.logout, name='logout'),
    #urls for projects view
    url(r'^(?P<user_id>\d+)/allprojects/$', views.allProjects, name='allProjects'),
    url(r'^(?P<user_id>\d+)/ownprojects/$', views.ownProjects, name='ownprojects'),
    url(r'^(?P<user_id>\d+)/collaboprojects/$', views.collabiratedProjects, name='collaboratedprojects'),
    #urls for issues view  
    url(r'^(?P<user_id>\d+)/allissues/$', views.allIssues, name='allIssues'),
    url(r'^(?P<user_id>\d+)/assignedissues/$', views.assignedIssues, name='assignedIssues'),
    url(r'^(?P<user_id>\d+)/assignToIssues/$', views.assignToIssues, name='assignToIssues'),
)
