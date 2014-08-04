from django.db import models
import datetime
from django.utils import timezone
#default=timezone.now

class Users(models.Model):
	name = models.CharField(max_length = 200)
	e_mail = models.EmailField(max_length = 200)
	password = models.CharField(max_length = 200)
	mobile_number = models.CharField(max_length = 200,blank=True)
	entry_date = models.DateTimeField(default=timezone.now)
	activationCode= models.CharField(max_length = 200)
	activationStatus = models.CharField(max_length = 100,  default = 'disable')	
	login_status = models.CharField(max_length = 100,  default = 'log_out')

	def __unicode__(self):
		return self.name


class Project_details(models.Model):
	project_owner = models.ForeignKey('Users',on_delete = models.CASCADE)
	title = models.CharField(max_length = 200)
	description = models.TextField(max_length = 20000)
	date_of_creation = models.DateTimeField(default=timezone.now)

	def __unicode__(self):
		return self.title


class Project_assignment(models.Model):
	project = models.ForeignKey('Project_details',on_delete = models.CASCADE)
	project_member = models.ForeignKey('Users',on_delete = models.CASCADE)	



class Issue(models.Model):
	project = models.ForeignKey('Project_details',on_delete = models.CASCADE)
	assigner = models.ForeignKey('Users',on_delete = models.CASCADE)
	title = models.CharField(max_length = 200)
	description = models.TextField(max_length = 20000)
	type_of_issue = models.CharField(max_length = 20)
	priority = models.CharField(max_length = 20)
	date_of_issue_creation = models.DateTimeField(default=timezone.now)

	def __unicode__(self):
		return self.title

class Issue_assignment(models.Model):
	assignee = models.ForeignKey('Users',on_delete = models.CASCADE)
	issue = models.ForeignKey('Issue',on_delete = models.CASCADE)	



class Comments(models.Model):
	issue = models.ForeignKey('Issue',on_delete = models.CASCADE)
	commenter = models.ForeignKey('Users',on_delete = models.CASCADE)
	description = models.TextField(max_length = 20000)
	date_of_comment = models.DateTimeField(default=timezone.now)


class Issue_status(models.Model):
	status_changer = models.ForeignKey('Users',on_delete = models.CASCADE)	
	issue = models.ForeignKey('Issue',on_delete = models.CASCADE)
	status = models.CharField(max_length = 20)
	date_of_change_status = models.DateTimeField(default=timezone.now)

	def __unicode__(self):
		return self.status



