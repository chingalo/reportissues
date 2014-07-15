from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from project.models import *
from project.forms import *

#return the home page for the site
def index(request):
			
	context = {}
	return render(request,'index.html',context)
	
#sign up for new account
def signUp(request):
		
	form = request.POST	
	firstName  = form.getlist('firstName')
	middleName = form.getlist('middleName')
	lastName = form.getlist('lastName')
	password = form.getlist('password')
	email = form.getlist('email')
	mobileNumber = form.getlist('mobileNumber')	
	
	#newUser = User()
		
	context = {}
	return render(request,'index.html',context)
	
		
	
#processing login processs
def login(request):
	
	userFromSystem = Users.objects.all()
	word = ''	
	
	if request.POST:
		#taking values from form		
		form = request.POST		
		emailListPosted = form.getlist('email')
		passwordPosted = form.getlist('password')
				
		#check if login user is registered
		for user in userFromSystem:
			if user.e_mail == emailListPosted[0] and user.password == passwordPosted[0]:
				#for registered user				
				user.login_status = "log_in"
				user.save()
				allProjects = []
				
				#list of projects for a given user
				allProjectsFromSystem = Project_details.objects.all()
				assignedProjectsFromSystem = Project_assignment.objects.all();
				for project in allProjectsFromSystem:
					if project.project_owner == user:
						allProjects.append(project)
				for projectLink in assignedProjectsFromSystem:
					if projectLink.project_member == user:
						allProjects.append(projectLink.project)			
							
				context = {'user':user,'contents':'allProjects','allProjects':allProjects}
				return render(request,'userFunction.html',context)
			
		#for not registered users
	word = 'Fail to login, if you are registered user try to login again else signup for new user account'		
	context = {'word':word,}
	return render(request,'index.html',context)


#all projects in the system
def allProjects(request,user_id):
	user = Users.objects.get(id = user_id)
	
	#checking if current user has login first
	if user.login_status =='log_out':
		word = 'You have not login in the system, please login first!'
		context = {'word':word,}	
		return render(request,'index.html',context)
		
	else:
		
		#list of all projects for a given user
		allProjectsFromSystem = Project_details.objects.all()
		assignedProjectsFromSystem = Project_assignment.objects.all()
		allProjects = []
		for project in allProjectsFromSystem:
			if project.project_owner == user:
				allProjects.append(project)
		for projectLink in assignedProjectsFromSystem:
			if projectLink.project_member == user:
				allProjects.append(projectLink.project)	
				
		context = {'user':user,'contents':'allProjects','allProjects':allProjects}	
		return render(request,'userFunction.html',context)


#own projects
def ownProjects(request,user_id):
	user = Users.objects.get(id = user_id)
	
	#checking if current user has login first
	if user.login_status =='log_out':
		word = 'You have not login in the system, please login first!'
		context = {'word':word,}	
		return render(request,'index.html',context)
		
	else:
		
		#list of all projects for a given user
		allProjectsFromSystem = Project_details.objects.all()
		allProjects = []
		for project in allProjectsFromSystem:
			if project.project_owner == user:
				allProjects.append(project)
						
		context = {'user':user,'contents':'ownProjects','allProjects':allProjects}	
		return render(request,'userFunction.html',context)

#collaborated projects
def collabiratedProjects(request,user_id):
	user = Users.objects.get(id = user_id)
	
	#checking if current user has login first
	if user.login_status =='log_out':
		word = 'You have not login in the system, please login first!'
		context = {'word':word,}	
		return render(request,'index.html',context)
		
	else:
		
		#list of all projects for a given user
		assignedProjectsFromSystem = Project_assignment.objects.all()
		allProjects = []		
		for projectLink in assignedProjectsFromSystem:
			if projectLink.project_member == user:
				allProjects.append(projectLink.project)	
				
		context = {'user':user,'contents':'collaboprojects','allProjects':allProjects}	
		return render(request,'userFunction.html',context)



#view individual project
def singleProject(request,user_id,project_id):
	
	user = Users.objects.get(id = user_id)
		
	#checking if current user has login first
	if user.login_status =='log_out':
		word = 'You have not login in the system, please login first!'
		context = {'word':word,}	
		return render(request,'index.html',context)
		
	else:	
		
		project = Project_details.objects.get(id = project_id)
		context = {'user':user,'contents':'singleproject','project':project}
		return render(request, 'userFunction.html',context)



#view all issues
def allIssues(request,user_id):
	user = Users.objects.get(id = user_id)
	
	#checking if current user has login first
	if user.login_status =='log_out':
		word = 'You have not login in the system, please login first!'
		context = {'word':word,}	
		return render(request,'index.html',context)
		
	else:		
		#list issues
		allOwnIssuesFromSystem = Issue.objects.all()
		allAssignedIssuesFromSystem = Issue_assignment.objects.all()
		allIssuesStatusFromSystem = Issue_status.objects.all()
		issues = []				
		for issue in allOwnIssuesFromSystem:
			if issue.assigner == user:
				issues.append(issue)
		
		for issue in allAssignedIssuesFromSystem:
			if issue.assignee == user:
				issues.append(issue.issue)		
				
		context = {'user':user,'contents':'allIssues','allIssues':issues,}	
		return render(request,'userFunction.html',context)


#view assigned issues
def assignedIssues(request,user_id):
	user = Users.objects.get(id = user_id)
	
	#checking if current user has login first
	if user.login_status =='log_out':
		word = 'You have not login in the system, please login first!'
		context = {'word':word,}	
		return render(request,'index.html',context)
		
	else:		
		#list issues
		allAssignedIssuesFromSystem = Issue_assignment.objects.all()
		issues = []			
		for issue in allAssignedIssuesFromSystem:
			if issue.assignee == user:
				issues.append(issue.issue)		
				
		context = {'user':user,'contents':'assignedIssues','assignedIssues':issues}	
		return render(request,'userFunction.html',context)

#view for assign to issues
def assignToIssues(request,user_id):
	user = Users.objects.get(id = user_id)
	
	#checking if current user has login first
	if user.login_status =='log_out':
		word = 'You have not login in the system, please login first!'
		context = {'word':word,}	
		return render(request,'index.html',context)
		
	else:		
		#list issues
		allOwnIssuesFromSystem = Issue.objects.all()		
		issues = []
		
		for issue in allOwnIssuesFromSystem:
			if issue.assigner == user:
				issues.append(issue)
				
				
		context = {'user':user,'contents':'assignToIssues','assignToIssues':issues}	
		return render(request,'userFunction.html',context)
		
		
#view individual issue
def singleIssue(request,user_id,issue_id):
	
	user = Users.objects.get(id = user_id)
		
	#checking if current user has login first
	if user.login_status =='log_out':
		word = 'You have not login in the system, please login first!'
		context = {'word':word,}	
		return render(request,'index.html',context)
		
	else:		
		#taking all comments , status and issues for a given
		commentsFromSystem = Comments.objects.all()		
		issuesStatusFromSystem = Issue_status.objects.all()
		issue = Issue.objects.get(id = issue_id) 
		
		comments = []
		status_log = []
		
		for comment in commentsFromSystem:
			if comment.issue == issue:
				comments.append(comment)		
		
		commentsTotal = len(comments)
		context = {'user':user,'contents':'singleissue','issue':issue,'commentsTotal':commentsTotal,'status_log':status_log,'comments':comments}
		return render(request, 'userFunction.html',context)

		

#log out process
def logout(request,user_id):
	#for successfull log out process	
	user = Users.objects.get(id = user_id)
	user.login_status = "log_out"
	user.save()
	
	return HttpResponseRedirect("/")







