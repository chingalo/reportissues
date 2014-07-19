from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
import json 
from project.models import *
from project.forms import *
from random import randrange

#return the home page for the site
def index(request):		
	
	captureValue = randrange(100000,999999)	
	context = {'captureValue':captureValue}	
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
	
	#activationCodeFromSystem = randrange(100000,999999)	
	#disable
	newUser = Users()
	newUser.name = firstName[0] + " " + middleName[0]+ " " +lastName[0]
	newUser.e_mail = email[0]
	newUser
	newUser
	newUser.mobile_number = mobileNumber[0]
	newUser.password = password[0]
	newUser.login_status = 'log_in'	
	newUser.save()
	
	#list of projects for a given user	
	assignedProjectsFromSystem = Project_assignment.objects.all();
	allProjects = []
	
	for projectLink in assignedProjectsFromSystem:
		if projectLink.project_member == newUser:
			allProjects.append(projectLink.project)	
		
	
	userName = firstName[0]
	
	context = {'user':newUser,'userName':userName,'contents':'allProjects','allProjects':allProjects}
	return render(request,'userFunction.html',context)
	
	
	
#view  profile
def viewProfile(request,user_id):
	user = Users.objects.get(id = user_id)
	
	nameList = user.name.split(" ")	
	userName = nameList[0]
	
	context = {'user':user,'userName':userName,'contents':'viewProfile',}
	return render(request,'userFunction.html',context)	





		
#edit profile
def editProfile(request,user_id):
	user = Users.objects.get(id = user_id)
	
	#checking if current user has login first
	if user.login_status =='log_out':
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue}	
		return render(request,'index.html',context)
		
	else:
		#prepare contents for redirect			
		if request.POST:		
			form = request.POST
			
			firstName  = form.getlist('firstName')
			middleName = form.getlist('middleName')
			lastName = form.getlist('lastName')
			password = form.getlist('password')
			mobileNumber = form.getlist('mobileNumber')
			
			user.name = firstName[0] + " " + middleName[0]+ " " +lastName[0]			
			user.mobile_number = mobileNumber[0]
			user.password = password[0]	
			user.save()
			
			nameList = user.name.split(" ")	
			userName = nameList[0]
			
			context = {'user':user,'userName':userName,'contents':'viewProfile',}
			return render(request,'userFunction.html',context)
			
		else:
			
			nameList = user.name.split(" ")	
			nameListCounter = len(nameList)
			middleName = ''
			
			if nameListCounter == 2:
				lastName = nameList[1]
			else:
				middleName = nameList[1]
				lastName = nameList[2]	
			userName = 	nameList[0]	
				
			context = {'user':user,'lastName':lastName,'middleName':middleName,'nameList':nameList,'nameListCounter':nameListCounter,'userName':userName,'contents':'editProfile',}
			return render(request, 'userFunction.html',context)
				

	
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
				
				nameList = user.name.split(" ")	
				userName = 	nameList[0]		
							
				context = {'user':user, 'userName':userName,'contents':'allProjects','allProjects':allProjects}
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
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue}	
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
					
		nameList = user.name.split(" ")	
		userName = 	nameList[0]			
		context = {'user':user,'userName':userName,'contents':'allProjects','allProjects':allProjects}	
		return render(request,'userFunction.html',context)


#own projects
def ownProjects(request,user_id):
	user = Users.objects.get(id = user_id)
	
	#checking if current user has login first
	if user.login_status =='log_out':
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue}	
		return render(request,'index.html',context)
		
	else:
		
		#list of all projects for a given user
		allProjectsFromSystem = Project_details.objects.all()
		allProjects = []
		for project in allProjectsFromSystem:
			if project.project_owner == user:
				allProjects.append(project)
				
		nameList = user.name.split(" ")	
		userName = 	nameList[0]	
						
		context = {'user':user,'userName':userName,'contents':'ownProjects','allProjects':allProjects}	
		return render(request,'userFunction.html',context)



#collaborated projects
def collabiratedProjects(request,user_id):
	user = Users.objects.get(id = user_id)
	
	#checking if current user has login first
	if user.login_status =='log_out':
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue}	
		return render(request,'index.html',context)
		
	else:
		
		#list of all projects for a given user
		assignedProjectsFromSystem = Project_assignment.objects.all()
		allProjects = []		
		for projectLink in assignedProjectsFromSystem:
			if projectLink.project_member == user:
				allProjects.append(projectLink.project)	
		
		nameList = user.name.split(" ")	
		userName = 	nameList[0]	
				
		context = {'user':user,'userName':userName,'contents':'collaboprojects','allProjects':allProjects}	
		return render(request,'userFunction.html',context)



#create new project
def createProject(request,user_id):
	user = Users.objects.get(id = user_id)
		
	#checking if current user has login first
	if user.login_status =='log_out':
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue}	
		return render(request,'index.html',context)
		
	else:	
		
		if request.POST:
			
			#taking values from form and create new project
			form = request.POST		
			titleOfTitle = form.getlist('title')
			descriptionOfTitle = form.getlist('description')
			
			newProject = Project_details()
			newProject.project_owner  = user		
			newProject.title = titleOfTitle[0]
			newProject.description = descriptionOfTitle[0]
			newProject.save()			
				
			
			#prepare contents for redirect
			allProjects = Project_details.objects.filter(project_owner = user)
			
			nameList = user.name.split(" ")	
			userName = 	nameList[0]
			
			context = {'user':user,'userName':userName,'contents':'ownProjects','allProjects':allProjects}	
			return render(request,'userFunction.html',context)
		
		else:
					
		
			nameList = user.name.split(" ")	
			userName = 	nameList[0]	
			
			context = {'user':user,'userName':userName,'contents':'createPorject',}
			return render(request, 'userFunction.html',context)
	


#edit project
def editProject(request,user_id,project_id):
	
	user = Users.objects.get(id = user_id)
		
	#checking if current user has login first
	if user.login_status =='log_out':
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue}	
		return render(request,'index.html',context)
		
	else:	
		project = Project_details.objects.get(id = project_id)
		
		if request.POST:						
						 
			#taking values from form and create new project
			form = request.POST		
			titleOfTitle = form.getlist('title')
			descriptionOfTitle = form.getlist('description')			
					
			project.title = titleOfTitle[0]
			project.description = descriptionOfTitle[0]
						
			project.save()
			
			nameList = user.name.split(" ")	
			userName = 	nameList[0]	
			
			context = {'user':user,'userName':userName,'contents':'singleproject','project':project}
			return render(request, 'userFunction.html',context)
			
		else:	
		
			nameList = user.name.split(" ")	
			userName = 	nameList[0]	
			
			context = {'user':user,'userName':userName,'contents':'editPorject','project':project,}
			return render(request, 'userFunction.html',context)



#view individual project
def singleProject(request,user_id,project_id):
	
	user = Users.objects.get(id = user_id)
		
	#checking if current user has login first
	if user.login_status =='log_out':
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue}	
		return render(request,'index.html',context)
		
	else:	
		
		nameList = user.name.split(" ")	
		userName = 	nameList[0]	
		
		project = Project_details.objects.get(id = project_id)		
		assignmentList = Project_assignment.objects.filter(project = project)
		memberList = []
		
		for assignment in assignmentList:
			memberList.append(assignment.project_member)
		
		context = {'user':user,'userName':userName,'memberList':memberList,'contents':'singleproject','project':project}
		return render(request, 'userFunction.html',context)


#add collaborator in the project
def addCollaborator(request,user_id,project_id):
	user = Users.objects.get(id = user_id)
	
	users = Users.objects.all()
	userListData = []
	
	for userInList in users:
		userListData.append(userInList.name)
		
	userList = json.dumps(userListData)	
	#checking if current user has login first
	if user.login_status =='log_out':
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue}	
		return render(request,'index.html',context)
		
	else:
		#for login user	
		nameList = user.name.split(" ")	
		userName = 	nameList[0]
		project = Project_details.objects.get(id = project_id)	
		
		if request.POST:
			form = request.POST			
			nameOfFrom = form.getlist('nameOfCollaborator')
			
			nameOfCollaborator = Users.objects.get(name = nameOfFrom[0])
			mewProjectAssignment = Project_assignment()
			mewProjectAssignment.project = project
			mewProjectAssignment.project_member = nameOfCollaborator
			mewProjectAssignment.save()	
			
			nameList = user.name.split(" ")	
			userName = 	nameList[0]
			
			context = {'user':user,'userName':userName,'contents':'singleproject','project':project}
			return render(request, 'userFunction.html',context)		
			
		else:	
			
			
			context = {'user':user,'userName':userName,'contents':'addCollaborator','project':project,'userList':userList}
			return render(request, 'userFunction.html',context)


#view all issues
def allIssues(request,user_id):
	user = Users.objects.get(id = user_id)

	#checking if current user has login first
	if user.login_status =='log_out':
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue}	
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
		
		nameList = user.name.split(" ")	
		userName = 	nameList[0]			

		context = {'user':user,'userName':userName,'contents':'allIssues','allIssues':issues,}	
		return render(request,'userFunction.html',context)


#view assigned issues
def assignedIssues(request,user_id):
	user = Users.objects.get(id = user_id)

	#checking if current user has login first
	if user.login_status =='log_out':
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue}	
		return render(request,'index.html',context)

	else:		
		#list issues
		allAssignedIssuesFromSystem = Issue_assignment.objects.all()
		issues = []			
		for issue in allAssignedIssuesFromSystem:
			if issue.assignee == user:
				issues.append(issue.issue)		

		nameList = user.name.split(" ")	
		userName = 	nameList[0]	
		
		context = {'user':user,'userName':userName,'contents':'assignedIssues','assignedIssues':issues}	
		return render(request,'userFunction.html',context)


#view for assign to issues
def assignToIssues(request,user_id):
	user = Users.objects.get(id = user_id)

	#checking if current user has login first
	if user.login_status =='log_out':
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue}	
		return render(request,'index.html',context)

	else:		
		#list issues
		allOwnIssuesFromSystem = Issue.objects.all()		
		issues = []

		for issue in allOwnIssuesFromSystem:
			if issue.assigner == user:
				issues.append(issue)

		nameList = user.name.split(" ")	
		userName = 	nameList[0]	
		
		context = {'user':user,'userName':userName,'contents':'assignToIssues','assignToIssues':issues}	
		return render(request,'userFunction.html',context)
		

#craete new issue and assign to user
def createIssue(request,user_id,project_id):
	user = Users.objects.get(id = user_id)

	
	#checking if current user has login first
	if user.login_status =='log_out':
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue}	
		return render(request,'index.html',context)

	else:
		#for login user	
		nameList = user.name.split(" ")	
		userName = 	nameList[0]
		project = Project_details.objects.get(id = project_id)	
		memberList = []
		 
		memberList.append(project.project_owner)
		
		assignmentList = Project_assignment.objects.filter(project = project)
		for assignment in assignmentList:
			memberList.append(assignment.project_member)

		if request.POST:
			form = request.POST	
			
			assignee = form.getlist('assignee')		
			aasignedUser = Users.objects.get(name = assignee[0])
			typeOfIssue = form.getlist('type')
			priority = form.getlist('priority')
			titleOfIssue = form.getlist('title')
			descriptionOfIssue = form.getlist('description')
			
			#new issue
			newIssue = Issue()
			newIssue.project = project
			newIssue.assigner = user
			newIssue.title = titleOfIssue[0]
			newIssue.description = descriptionOfIssue[0]
			newIssue.type_of_issue = typeOfIssue[0]
			newIssue.priority = priority[0]
			newIssue.save()
			
			#new issue status
			newStatus = Issue_status()
			newStatus.status_changer = user
			newStatus.issue = newIssue
			newStatus.status = "new"
			newStatus.save()
			
			#new issue assignments
			newAssignment = Issue_assignment()
			newAssignment.assignee = aasignedUser
			newAssignment.issue = newIssue
			newAssignment.save()
			
			#prepare redirect process
			issues = Issue.objects.filter(assigner = user)
			
			nameList = user.name.split(" ")	
			userName = 	nameList[0]

			context = {'user':user,'userName':userName,'contents':'assignToIssues','assignToIssues':issues}	
			return render(request,'userFunction.html',context)		

		else:	


			context = {'user':user,'userName':userName,'contents':'createIssue','project':project,'memberList':memberList}
			return render(request, 'userFunction.html',context)

		
#view individual issue
def singleIssue(request,user_id,issue_id):
	
	user = Users.objects.get(id = user_id)
		
	#checking if current user has login first
	if user.login_status =='log_out':
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue}	
		return render(request,'index.html',context)
		
	else:		
		#taking all comments , status and issues for a given		
		issue = Issue.objects.get(id = issue_id) 
		commentsFromSystem = Comments.objects.filter(issue = issue)		
		issuesStatusFromSystem = Issue_status.objects.filter(issue = issue).order_by('-date_of_change_status')		 
		issuesAssignmentsFromSystem = Issue_assignment.objects.all()
			
		
		comments = commentsFromSystem
		status_log = issuesStatusFromSystem	
		
		issuesAssignmentsFromSystem = issuesAssignmentsFromSystem = Issue_assignment.objects.all()
		for issuesAssignment in issuesAssignmentsFromSystem:
			if issuesAssignment.issue == issue:
				issueAssignee = issuesAssignment.assignee		
				
		commentsTotal = len(comments)
		nameList = user.name.split(" ")	
		userName = 	nameList[0]		
		
		
		context = {'user':user,'userName':userName,'contents':'singleissue','issueAssignee':issueAssignee,'issue':issue,'commentsTotal':commentsTotal,'status_log':status_log,'comments':comments}
		return render(request, 'userFunction.html',context)


#comments on issues
def commentOnIssue(request,user_id,issue_id):
	
	user = Users.objects.get(id = user_id)
		
	#checking if current user has login first
	if user.login_status =='log_out':
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue}	
		return render(request,'index.html',context)
		
	else:
		issue = Issue.objects.get(id = issue_id)
		#taking c
		commentForm = request.POST
		comment = commentForm.getlist('comments')
		
		commentToIssue = Comments()
		commentToIssue.issue = issue
		commentToIssue.commenter = user
		commentToIssue.description = comment[0]				
		commentToIssue.save()
			
		#taking all comments & status for a given ready for page redirect
		commentsFromSystem = Comments.objects.filter(issue = issue)		
		issuesStatusFromSystem = Issue_status.objects.filter(issue = issue).order_by('-date_of_change_status')		 
		issuesAssignmentsFromSystem = Issue_assignment.objects.all()
			
		
		comments = commentsFromSystem
		status_log = issuesStatusFromSystem	
		
		issuesAssignmentsFromSystem = issuesAssignmentsFromSystem = Issue_assignment.objects.all()
		for issuesAssignment in issuesAssignmentsFromSystem:
			if issuesAssignment.issue == issue:
				issueAssignee = issuesAssignment.assignee		
				
		commentsTotal = len(comments)
		nameList = user.name.split(" ")	
		userName = 	nameList[0]	
		context = {'user':user,'userName':userName,'contents':'singleissue','issueAssignee':issueAssignee,'issue':issue,'commentsTotal':commentsTotal,'status_log':status_log,'comments':comments}
		return render(request, 'userFunction.html',context)
		
#close issue
def closeIssue(request,user_id,issue_id):
	
	user = Users.objects.get(id = user_id)
		
	#checking if current user has login first
	if user.login_status =='log_out':
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue}	
		return render(request,'index.html',context)
		
	else:		
		issue = Issue.objects.get(id = issue_id)				
		status_log = []
		#previous status history
		issuesStatusFromSystem = Issue_status.objects.all()	
		for status in issuesStatusFromSystem:
			if status.issue == issue:
				status_log.append(status)
		
		numberOfStatus = len(status_log)
		if(status_log[numberOfStatus - 1].status != "close"):
			#change status of issue
			statusChange = Issue_status()
			statusChange.status_changer = user
			statusChange.issue = issue
			statusChange.status = "close"	
			statusChange.save()
			
		#taking all comments & status for a given ready for page redirect
		commentsFromSystem = Comments.objects.filter(issue = issue)		
		issuesStatusFromSystem = Issue_status.objects.filter(issue = issue).order_by('-date_of_change_status')		 
		issuesAssignmentsFromSystem = Issue_assignment.objects.all()
			
		
		comments = commentsFromSystem
		status_log = issuesStatusFromSystem	
		
		issuesAssignmentsFromSystem = issuesAssignmentsFromSystem = Issue_assignment.objects.all()
		for issuesAssignment in issuesAssignmentsFromSystem:
			if issuesAssignment.issue == issue:
				issueAssignee = issuesAssignment.assignee		
				
		commentsTotal = len(comments)
		nameList = user.name.split(" ")	
		userName = 	nameList[0]	
		context = {'user':user,'userName':userName,'contents':'singleissue','issueAssignee':issueAssignee,'issue':issue,'commentsTotal':commentsTotal,'status_log':status_log,'comments':comments}
		return render(request, 'userFunction.html',context)

#reopen issue		
def reopenIssue(request,user_id,issue_id):
	
	user = Users.objects.get(id = user_id)
		
	#checking if current user has login first
	if user.login_status =='log_out':
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue}	
		return render(request,'index.html',context)
		
	else:		
		issue = Issue.objects.get(id = issue_id)				
		status_log = []
		#previous status history
		issuesStatusFromSystem = Issue_status.objects.all()	
		for status in issuesStatusFromSystem:
			if status.issue == issue:
				status_log.append(status)
		
		numberOfStatus = len(status_log)
		if(status_log[numberOfStatus - 1].status != "reopen"):
			#change status of issue
			statusChange = Issue_status()
			statusChange.status_changer = user
			statusChange.issue = issue
			statusChange.status = "reopen"	
			statusChange.save()
			
		#taking all comments & status for a given ready for page redirect
		commentsFromSystem = Comments.objects.filter(issue = issue)		
		issuesStatusFromSystem = Issue_status.objects.filter(issue = issue).order_by('-date_of_change_status')		 
		issuesAssignmentsFromSystem = Issue_assignment.objects.all()	
		
		comments = commentsFromSystem
		status_log = issuesStatusFromSystem			
		issuesAssignmentsFromSystem = issuesAssignmentsFromSystem = Issue_assignment.objects.all()
		for issuesAssignment in issuesAssignmentsFromSystem:
			if issuesAssignment.issue == issue:
				issueAssignee = issuesAssignment.assignee
				
		commentsTotal = len(comments)
		nameList = user.name.split(" ")	
		userName = 	nameList[0]	
		context = {'user':user,'userName':userName,'contents':'singleissue','issueAssignee':issueAssignee,'issue':issue,'commentsTotal':commentsTotal,'status_log':status_log,'comments':comments}
		return render(request, 'userFunction.html',context)




#log out process
def logout(request,user_id):
	#for successfull log out process	
	user = Users.objects.get(id = user_id)
	user.login_status = "log_out"
	user.save()
	
	return HttpResponseRedirect("/")







