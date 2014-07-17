from django.conf.urls import patterns, url

from project import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.signUp, name='signUp'),
    url(r'^login/$', views.login, name='login'),
    url(r'^(?P<user_id>\d+)/editProfile/$', views.editProfile, name='editProfile'),
    url(r'^(?P<user_id>\d+)/viewProfile/$', views.viewProfile, name='viewProfile'),
    url(r'^(?P<user_id>\d+)/logout/$', views.logout, name='logout'),
    #urls for projects view
    url(r'^(?P<user_id>\d+)/allprojects/$', views.allProjects, name='allProjects'),
    url(r'^(?P<user_id>\d+)/ownprojects/$', views.ownProjects, name='ownprojects'),
    url(r'^(?P<user_id>\d+)/collaboprojects/$', views.collabiratedProjects, name='collaboratedprojects'),
    #urls for issues view  
    url(r'^(?P<user_id>\d+)/allissues/$', views.allIssues, name='allIssues'),
    url(r'^(?P<user_id>\d+)/assignedissues/$', views.assignedIssues, name='assignedIssues'),
    url(r'^(?P<user_id>\d+)/assignToIssues/$', views.assignToIssues, name='assignToIssues'),
    #urls for individual project 
    url(r'^(?P<user_id>\d+)/(?P<project_id>\d+)/addCollaborator/$', views.addCollaborator, name='addCollaborator'),    
    url(r'^(?P<user_id>\d+)/(?P<project_id>\d+)/singleProject/$', views.singleProject, name='singleProject'),
    url(r'^(?P<user_id>\d+)/(?P<project_id>\d+)/editProject/$', views.editProject, name='editProject'),
    url(r'^(?P<user_id>\d+)/createProject/$', views.createProject, name='createProject'),
    #urls for individual issue
    url(r'^(?P<user_id>\d+)/(?P<issue_id>\d+)/singleIssue/$', views.singleIssue, name='singleIssue'),
    url(r'^(?P<user_id>\d+)/(?P<issue_id>\d+)/comment/$', views.commentOnIssue, name='commentOnIssue'),
    url(r'^(?P<user_id>\d+)/(?P<issue_id>\d+)/closeIssue/$', views.closeIssue, name='closeIssue'),
    url(r'^(?P<user_id>\d+)/(?P<issue_id>\d+)/reopenIssue/$', views.reopenIssue, name='reopenIssue'),
    
    
)
