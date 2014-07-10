from django.db import models
import datetime
from django.utils import timezone
#default=timezone.now

class Users(models.Model):
	name = models.CharField(max_length = 200)
	e_mail = models.EmailField(max_length = 200)
	password = models.CharField(max_length = 200)
	mobile_number = models.CharField(max_length = 200)
	entry_date = models.DateTimeField()
	login_status = models.CharField(max_length = 100,  default = 'log_out')
	
	def __unicode__(self):
		return self.name

class Project_details(models.Model):
	project_owner = models.ForeignKey('Users',on_delete = models.CASCADE)
	title = models.CharField(max_length = 200)
	description = models.TextField(max_length = 20000)
	date_of_creation = models.DateTimeField()
	
	def __unicode__(self):
		return self.title
	
class Project_assignment(models.Model):
	project = models.ForeignKey('Project_details',on_delete = models.CASCADE)
	project_member = models.ForeignKey('Users',on_delete = models.CASCADE)	
	
class Issue(models.Model):
	project = models.ForeignKey('Project_details',on_delete = models.CASCADE)
	title = models.CharField(max_length = 200)
	description = models.TextField(max_length = 20000)
	type_of_issue = models.CharField(max_length = 20)
	priority = models.CharField(max_length = 20)
	
	def __unicode__(self):
		return self.title
		
	
	
	
	
	
	
	
	
	
	
