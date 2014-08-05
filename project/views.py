from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
import json 
from django.core.mail import send_mail
from project.models import *
from random import randrange
from datetime import datetime
# time   str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


#return the home page for the site
def index(request):		
	users = Users.objects.all()
	userList = []
	userEmailData =[]
	for user in users:
		userList.append(user.e_mail)
		userEmailData = json.dumps(userList)
		
	captureValue = randrange(100000,999999)	
	context = {'captureValue':captureValue,'userEmailData':userEmailData}	
	return render(request,'index.html',context)





#request change password
def forgetPassword(request):
	users = Users.objects.all()
	allUserEmails = []
	allemails = []
	for user in users:
		allUserEmails.append(user.e_mail)
		allemails = json.dumps(allUserEmails)
		
	if request.POST:
		
		form = request.POST
		emailForRequestNewPassword = form.getlist('emailForRequestNewPassword')
		userRequestNewPassword = Users.objects.get(e_mail = emailForRequestNewPassword[0])
		#send emils for request new password
		send_mail('REQUEST TO CHANGE PASSWORD IN IMS', 'Hi ' +userRequestNewPassword.name+',\nYou have request to change new password in IMS.\nIf you are sure want to change your password click on link below.\n\nhttp://issuesmanager.herokuapp.com/'+str(userRequestNewPassword.id)+'/changePassword/'+'\n\n\nRegard,\nIMS developer,\nJoseph Chingalo,\nSoftware Consultant at Unyayo Systems Limited,\nMobile Number: +255687168637.', '',[emailForRequestNewPassword[0]], fail_silently=False)	
		
		users = Users.objects.all()
		userList = []
		userEmailData =[]
		for user in users:
			userList.append(user.e_mail)
			userEmailData = json.dumps(userList)
			
		captureValue = randrange(100000,999999)	
		context = {'captureValue':captureValue,'userEmailData':userEmailData}	
		return render(request,'index.html',context)
	
	else:
		context = {'contents':'forgetPassword','allemails':allemails}
		return render(request,'newpassword.html',context)
	





#chenge password
def changePassword(request,user_id):
	user = Users.objects.get(id = user_id)
	
	if request.POST:
		form = request.POST
		newPassword = form.getlist('newPassword')
		user.password = newPassword[0]
		user.save()
		#send emils for request new password
		send_mail('SUCCESSFUL UPDATE ON PASSWORD IN IMS', 'Hi ' + user.name + '\nYou have successful update your password.\nYour new password is \"'+str(user.password)+' \" \n\nRegard,\nIMS developer,\nJoseph Chingalo,\nSoftware Consultant at Unyayo Systems Limited,\nMobile Number: +255687168637.', '',[user.e_mail], fail_silently=False)	
		
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
	
	context = {'contents':'changePassword','user':user}
	return render(request,'newpassword.html',context)
		






	
#sign up for new account
def signUp(request):
		
	form = request.POST	
	firstName  = form.getlist('firstName')
	middleName = form.getlist('middleName')
	lastName = form.getlist('lastName')
	password = form.getlist('password')
	email = form.getlist('email')
	mobileNumber = form.getlist('mobileNumber')	
	
	
	newUser = Users()
	newUser.name = firstName[0] + " " + middleName[0]+ " " +lastName[0]
	newUser.e_mail = email[0]
	newUser.activationCode = randrange(99999,99999999)	
	newUser.mobile_number = mobileNumber[0]
	newUser.password = password[0]
	newUser.login_status = 'log_in'	
	newUser.save()
	
	#email for activation codes
	subject = "WELCOME TO ISSUES MANAGEMENT SYSTEM (IMS)"
	message = "hi, "+newUser.name+"\nYou hava successful create new account in IMS. You are welcome to IMS, its open source system aims to facilitate easy management of your software development as well as software maintenance through tracking issues related to a given project.\nTo activate your account please login into your account, click on activation account link and fill activation codes below.\nActivation code : " + str(newUser.activationCode) + "\n\nRegard,\nIMS developer,\nJoseph Chingalo,\nSoftware Consultant at Unyayo Systems Limited,\nMobile Number: +255687168637."
	recipient_list = [newUser.e_mail]	
	from_email = 'josephchingalo@gmail.com'
	send_mail(subject,message,from_email,recipient_list,fail_silently=False)
	
	
	#list of projects for a given user	
	assignedProjectsFromSystem = Project_assignment.objects.all();
	allProjects = []

	for projectLink in assignedProjectsFromSystem:
		if projectLink.project_member == newUser:
			allProjects.append(projectLink.project)	


	userName = firstName[0]

	context = {'user':newUser,'userName':userName,'contents':'allProjects','allProjects':allProjects}
	return render(request,'userFunction.html',context)
	



#activate account
def acctivationAccount(request,user_id):
	user = Users.objects.get(id = user_id)
	
	if request.POST:		
		form = request.POST
		
		activationCode = form.getlist('activationcode')
		if user.activationCode == activationCode[0]:
			user.activationStatus = 'enable'			
			user.save()
			#send activation complete email
			subject = "SUCCESSFULLY ACCOUNT ACTIVATION IN IMS"
			message = "Hi ,"+user.name +"\nYou have successfully activate your account. You can now create your project, add or invite collaborators and creates issues."+"\n\nRegard,\nIMS developer,\nJoseph Chingalo,\nSoftware Consultant at Unyayo Systems Limited,\nMobile Number: +255687168637."
			recipient_list = []
			recipient_list.append(user.e_mail)
			from_email = 'no-reply@project.org'
			send_mail(subject,message,from_email,recipient_list,fail_silently=False)
			
			
			nameList = user.name.split(" ")	
			userName = nameList[0]
			context = {'user':user,'userName':userName,'contents':'allProjects','allProjects':allProjects}
			return render(request,'userFunction.html',context)
		else:
			context = {'user':user,'word':"Activation key does not match"}
			return render(request,'activation.html',context)
			
		
	else:
		context = {'user':user,}
		return render(request,'activation.html',context)
		

		
			
	
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
		users = Users.objects.all()
		userList = []
		for user in users:
			userList.append(user.e_mail)
		userEmailData = json.dumps(userList)
		
		
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue,'userEmailData':userEmailData}	
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
	users = Users.objects.all()
	userList = []
	for user in users:
		userList.append(user.e_mail)
	userEmailData = json.dumps(userList)
	
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
	
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue,'userEmailData':userEmailData,}	
		return render(request,'index.html',context)	
	word = 'Fail to login, if you are registered user try to login again else signup for new user account'		
	captureValue = randrange(100000,999999)	
	context = {'word':word,'captureValue':captureValue,'userEmailData':userEmailData}	
	return render(request,'index.html',context)






#all projects in the system
def allProjects(request,user_id):
	user = Users.objects.get(id = user_id)
	
	#checking if current user has login first
	if user.login_status =='log_out':
		users = Users.objects.all()
		userList = []
		for user in users:
			userList.append(user.e_mail)
		userEmailData = json.dumps(userList)
		
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue,'userEmailData':userEmailData}	
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
		users = Users.objects.all()
		userList = []
		for user in users:
			userList.append(user.e_mail)
		userEmailData = json.dumps(userList)
		
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue,'userEmailData':userEmailData}	
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
		users = Users.objects.all()
		userList = []
		for user in users:
			userList.append(user.e_mail)
		userEmailData = json.dumps(userList)
		
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue,'userEmailData':userEmailData}	
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
		users = Users.objects.all()
		userList = []
		for user in users:
			userList.append(user.e_mail)
		userEmailData = json.dumps(userList)
		
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue,'userEmailData':userEmailData}	
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
			
			#send email after create new project			
			subject = "SUCCESSFUL CREATION OF " + newProject.title + "project IN IMS"
			message = "Hi, "+user.name+"\nYour have successful create "+ newProject.title +" project at"+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+".\nFor easy management of your project you can add more collaborators and assign some issues." + "\n\nRegard,\nIMS developer,\nJoseph Chingalo,\nSoftware Consultant at Unyayo Systems Limited,\nMobile Number: +255687168637."

			recipient_list = []
			recipient_list.append(user.e_mail)
			from_email = 'no-reply@project.org'
			send_mail(subject,message,from_email,recipient_list,fail_silently=False)
			
				
			
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
		users = Users.objects.all()
		userList = []
		for user in users:
			userList.append(user.e_mail)
		userEmailData = json.dumps(userList)
		
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue,'userEmailData':userEmailData}	
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
			
			assignmentList = Project_assignment.objects.filter(project = project)
			
			memberList = []
			nameList = user.name.split(" ")	
			userName = 	nameList[0]	
			for assignment in assignmentList:
				memberList.append(assignment.project_member)
			
			projectOwner = project.project_owner
			
			
			context = {'user':user,'projectOwner':projectOwner,'memberList':memberList,'userName':userName,'contents':'singleproject','project':project}
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
		users = Users.objects.all()
		userList = []
		for user in users:
			userList.append(user.e_mail)
		userEmailData = json.dumps(userList)
		
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue,'userEmailData':userEmailData}	
		return render(request,'index.html',context)
		
	else:	
		
		nameList = user.name.split(" ")	
		userName = 	nameList[0]	
		
		project = Project_details.objects.get(id = project_id)		
		assignmentList = Project_assignment.objects.filter(project = project)
		memberList = []
		
		for assignment in assignmentList:
			memberList.append(assignment.project_member)
		
		projectOwner = project.project_owner
				
		context = {'user':user,'projectOwner':projectOwner,'userName':userName,'memberList':memberList,'contents':'singleproject','project':project}
		return render(request, 'userFunction.html',context)




#search and create new issue
def search(request,user_id):
	user = Users.objects.get(id = user_id)
	
	#checking if current user has login first
	if user.login_status =='log_out':
		users = Users.objects.all()
		userList = []
		for user in users:
			userList.append(user.e_mail)
		userEmailData = json.dumps(userList)
		
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue,'userEmailData':userEmailData}	
		return render(request,'index.html',context)
		
	else:
		if request.POST:
			
			form = request.POST
			nameOfProjectList = form.getlist('nameOfProject')
			
			project = Project_details.objects.get(title = nameOfProjectList[0])	
			
			collaboratorOfProject = []
			allProjectAssignments = Project_assignment.objects.all()
			
			for assignment in allProjectAssignments:
				if assignment.project == project:
					collaboratorOfProject.append(assignment.project_member)
			
			nameList = user.name.split(" ")	
			userName = 	nameList[0]
			
			context = {'user':user,'userName':userName,'contents':'selectedProject','collaboratorOfProject':collaboratorOfProject,'project':project}
			return render(request,'search.html',context)
				
		else:
			allProjectsFromSystem = Project_details.objects.all()
			projectList = []
			for project in allProjectsFromSystem:
				projectList.append(project.title)
			
			allProjects = json.dumps(projectList)
			
			nameList = user.name.split(" ")	
			userName = 	nameList[0]
			
			context = {'user':user,'userName':userName,'contents':'selectProject','allProjects':allProjects}
			return render(request,'search.html',context)





#confirm delete project
def deleteConfirmProject(request,user_id,project_id):
	user = Users.objects.get(id = user_id)
	project = Project_details.objects.get(id = project_id)	
	
	#checking if current user has login first
	if user.login_status =='log_out':
		users = Users.objects.all()
		userList = []
		for user in users:
			userList.append(user.e_mail)
		userEmailData = json.dumps(userList)
		
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue,'userEmailData':userEmailData}	
		return render(request,'index.html',context)
	else:
		nameList = user.name.split(" ")	
		userName = 	nameList[0]	
		
		context = {'user':user,'userName':userName,'contents':'deleteConfirmProject','project':project}
		return render(request, 'deleteConfirm.html',context)
		
			





#delete project
def deleteProject(request,user_id,project_id):
	user = Users.objects.get(id = user_id)		
	
	#checking if current user has login first
	if user.login_status =='log_out':
		users = Users.objects.all()
		userList = []
		for user in users:
			userList.append(user.e_mail)
		userEmailData = json.dumps(userList)
		
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue,'userEmailData':userEmailData}	
		return render(request,'index.html',context)
	else:
		project = Project_details.objects.get(id = project_id)
		
		#send email to user:
		subject = "SUCCESSFUL DELETION OF "+project.title+" project IN IMS"
		recipient_list = []
		recipient_list.append(user.e_mail)
		from_email = 'no-reply@project.org'
		message = "Hi ," + user.name + "\nYou have succeful deleted " + project.title + " project on " + str(datetime.now().strftime('%Y-%m-%d')) + " at " + str(datetime.now().strftime('%H:%M:%S')) + "\n\nRegard,\nIMS developer,\nJoseph Chingalo,\nSoftware Consultant at Unyayo Systems Limited,\nMobile Number: +255687168637."
		send_mail(subject,message,from_email,recipient_list,fail_silently=False)
		#to all collaborator
		
		projectAssignmentList = Project_assignment.objects.filter(project = project)
		recipient_list = []
		for projectAssignment in projectAssignmentList:
			recipient_list.append(projectAssignment.project_member.e_mail)			
		message = "Hi ,\n"+user.name +" have deleted " + project.title + " project on " + str(datetime.now().strftime('%Y-%m-%d')) + " at " + str(datetime.now().strftime('%H:%M:%S')) +".\nYou are no longer collaborator on " + project.title +  " project.\n\nRegard,\nIMS developer,\nJoseph Chingalo,\nSoftware Consultant at Unyayo Systems Limited,\nMobile Number: +255687168637."
		
		send_mail(subject,message,from_email,recipient_list,fail_silently=False)
		
		#delete project codes 		
		project.delete()
		
		
		nameList = user.name.split(" ")	
		userName = 	nameList[0]
		
		allProjects = Project_details.objects.filter(project_owner = user)
		
		context = {'user':user,'userName':userName,'contents':'ownProjects','allProjects':allProjects}	
		return render(request,'userFunction.html',context)	
		





#delete project confirmation
def deleteColaborationOnProjectConfirmation(request,user_id,project_id):
	user = Users.objects.get(id = user_id)
	project = Project_details.objects.get(id = project_id)	
	
	#checking if current user has login first
	if user.login_status =='log_out':
		users = Users.objects.all()
		userList = []
		for user in users:
			userList.append(user.e_mail)
		userEmailData = json.dumps(userList)
		
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue,'userEmailData':userEmailData}	
		return render(request,'index.html',context)
	else:
		nameList = user.name.split(" ")	
		userName = 	nameList[0]	
		
		context = {'user':user,'userName':userName,'contents':'deleteColaborationOnProjectConfirmation','project':project}
		return render(request, 'deleteConfirm.html',context)






#delete project collaboration 
def deleteColaborationOnProject(request,user_id,project_id):
	user = Users.objects.get(id = user_id)
	project = Project_details.objects.get(id = project_id)	
	
	#checking if current user has login first
	if user.login_status =='log_out':
		users = Users.objects.all()
		userList = []
		for user in users:
			userList.append(user.e_mail)
		userEmailData = json.dumps(userList)
		
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue,'userEmailData':userEmailData}	
		return render(request,'index.html',context)
	else:
		nameList = user.name.split(" ")	
		userName = 	nameList[0]	
		
		#send emails		
		subject = "COMPLETLY REMOVAL OF COLLABORATION ON "+project.title + "project IN IMS"		
		from_email = 'no-reply@project.org'
		recipient_list = []
		recipient_list.append(user.e_mail)		
		message = "Hi ,"+user.name +"\nYou have successful remove your collaboration on " + project.title + " project on " +  str(datetime.now().strftime('%Y-%m-%d')) + " at " + str(datetime.now().strftime('%H:%M:%S')) + "\n\nRegard,\nIMS developer,\nJoseph Chingalo,\nSoftware Consultant at Unyayo Systems Limited,\nMobile Number: +255687168637."
		send_mail(subject,message,from_email,recipient_list,fail_silently=False)
		
		recipient_list = []
		recipient_list.append(project.project_owner.e_mail)		
		message = "Hi ,"+project.project_owner.name +"\n" + user.name + " have removed collaraboration on "+project.title + " project on " + str(datetime.now().strftime('%Y-%m-%d')) + " at " + str(datetime.now().strftime('%H:%M:%S')) + "\n\nRegard,\nIMS developer,\nJoseph Chingalo,\nSoftware Consultant at Unyayo Systems Limited,\nMobile Number: +255687168637."
		send_mail(subject,message,from_email,recipient_list,fail_silently=False)
		
		
		#delete collaboration on project  project_member = user and 
		collaborationList = Project_assignment.objects.filter(project = project)
		
		for collaboration in collaborationList:
			if collaboration.project_member == user:
				collarationToBeRemoved = collaboration
				collarationToBeRemoved.delete()	
				break		
			
		assignedProjectsFromSystem = Project_assignment.objects.all()
		allProjects = []		
		for projectLink in assignedProjectsFromSystem:
			if projectLink.project_member == user:
				allProjects.append(projectLink.project)	

				
		context = {'user':user,'userName':userName,'contents':'collaboprojects','allProjects':allProjects}	
		return render(request,'userFunction.html',context)



		



#send invitation for collaboration
def sendInvitation(request,user_id,project_id):
	user = Users.objects.get(id = user_id)
	project = Project_details.objects.get(id = project_id)	
	
	users = Users.objects.all()
	projectAssigments = Project_assignment.objects.all()
	userListData = []	
	for userInList in users:		
		if user != userInList:
			userListData.append(userInList.name)			
		
	userList = json.dumps(userListData)	
	#checking if current user has login first
	if user.login_status =='log_out':
		users = Users.objects.all()
		userList = []
		for user in users:
			userList.append(user.e_mail)
		userEmailData = json.dumps(userList)
		
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue,'userEmailData':userEmailData}	
		return render(request,'index.html',context)
		
	else:
		#for login user	
		nameList = user.name.split(" ")	
		userName = 	nameList[0]
		if request.POST:
			form = request.POST
			inviteeEmail = form.getlist('emailOfInvitee')
			
			#checking for availabilities of user
			userAvailability = 0
			allUsers = Users.objects.all()
			for userToBeChecked in allUsers:
				if userToBeChecked.e_mail == inviteeEmail[0]:
					userAvailability = 1
			
			if userAvailability == 0 :
				
				newUser = Users()
				newUser.name = " "
				newUser.e_mail = inviteeEmail[0]
				newUser.mobile_number = ""
				newUser.password = randrange(1000,9999)	
				newUser.activationCode = randrange(100000,999999)	
				newUser.save()
				
				projectAssignment = Project_assignment()
				projectAssignment.project = project
				projectAssignment.project_member = newUser
				projectAssignment.save()
				
				#send email after add collaborator in the project
				subject = "COLLABORATION INVITATION ON "+project.title + " IN IMS"
				message = "Hi, \nWelcome to IMS system. Its tracking issue system aims to facilitates easy management of software development as well as software maintenance.\nYou have been invited as collaborator on "+project.title+" project" +"by "+ user.name+ "\nYour new password : "+ str(newUser.password) + "\nYour activation codes: " + str(newUser.activationCode) + "\nYou can login into IMS website on url below and edit your information\nhttp://issuesmanager.herokuapp.com/" + "\n\nRegard,\nIMS developer,\nJoseph Chingalo,\nSoftware Consultant at Unyayo Systems Limited,\nMobile Number: +255687168637."
				recipient_list = []
				recipient_list.append(inviteeEmail[0])
				from_email = 'no-reply@project.org'
				send_mail(subject,message,from_email,recipient_list,fail_silently=False)

				message = "Hi, "+user.name+"\nYou have successful invited  "+ inviteeEmail[0] +" as collaborator on "+project.title+" project" + "\n\nRegard,\nIMS developer,\nJoseph Chingalo,\nSoftware Consultant at Unyayo Systems Limited,\nMobile Number: +255687168637."
				recipient_list = []
				recipient_list.append(user.e_mail)
				from_email = 'no-reply@project.org'
				send_mail(subject,message,from_email,recipient_list,fail_silently=False)
			
			else:
				#if user exit
				invitee = Users.objects.get(e_mail = inviteeEmail[0])
				
				projectAssignment = Project_assignment()
				projectAssignment.project = project
				projectAssignment.project_member = invitee
				projectAssignment.save()
				
				#send email after add collaborator in the project
				subject = "COLLABORATION INVITATION ON "+project.title + " IN IMS"
				message = "Hi, " +invitee.name +"\nYou have been invited as collaborator on "+project.title+" project" +"by "+ user.name + "\n\nRegard,\nIMS developer,\nJoseph Chingalo,\nSoftware Consultant at Unyayo Systems Limited,\nMobile Number: +255687168637."
				recipient_list = []
				recipient_list.append(invitee.e_mail)
				from_email = 'no-reply@project.org'
				send_mail(subject,message,from_email,recipient_list,fail_silently=False)

				message = "Hi, "+user.name+"\nYou have successful invited  "+ invitee.name +" as collaborator on "+project.title+" project" + "\n\nRegard,\nIMS developer,\nJoseph Chingalo,\nSoftware Consultant at Unyayo Systems Limited,\nMobile Number: +255687168637."
				recipient_list = []
				recipient_list.append(user.e_mail)
				from_email = 'no-reply@project.org'
				send_mail(subject,message,from_email,recipient_list,fail_silently=False)
				
				
				
			nameList = user.name.split(" ")	
			userName = 	nameList[0]

			projectOwner = project.project_owner
			assignmentList = Project_assignment.objects.filter(project = project)
			memberList = []

			for assignment in assignmentList:
				memberList.append(assignment.project_member)

			context = {'user':user,'memberList':memberList,'projectOwner':projectOwner,'userName':userName,'contents':'singleproject','project':project}
			return render(request, 'userFunction.html',context)
		
		else:
			context = {'user':user,'userName':userName,'contents':'addCollaborator','project':project,'userList':userList}
			return render(request, 'userFunction.html',context)		
		
		
		
		
		




#add collaborator in the project
def addCollaborator(request,user_id,project_id):
	user = Users.objects.get(id = user_id)
	project = Project_details.objects.get(id = project_id)	
	
	users = Users.objects.all()
	projectAssigments = Project_assignment.objects.all()
	userListData = []	
	for userInList in users:		
		if user != userInList:
			userListData.append(userInList.name)			
		
	userList = json.dumps(userListData)	
	#checking if current user has login first
	if user.login_status =='log_out':
		users = Users.objects.all()
		userList = []
		for user in users:
			userList.append(user.e_mail)
		userEmailData = json.dumps(userList)
		
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue,'userEmailData':userEmailData}	
		return render(request,'index.html',context)
		
	else:
		#for login user	
		nameList = user.name.split(" ")	
		userName = 	nameList[0]		
		
		if request.POST:
			form = request.POST			
			nameOfFrom = form.getlist('nameOfCollaborator')
			
			Collaborator = Users.objects.get(name = nameOfFrom[0])
			mewProjectAssignment = Project_assignment()
			mewProjectAssignment.project = project
			mewProjectAssignment.project_member =Collaborator
			mewProjectAssignment.save()	
			
			#send email after add collaborator in the project
			subject = "COLLABORATION ON "+project.title + " IN IMS"
			message = "Hi, "+Collaborator.name+"\nYou have been add as collaborator on "+project.title+" project" + "\n\nRegard,\nIMS developer,\nJoseph Chingalo,\nSoftware Consultant at Unyayo Systems Limited,\nMobile Number: +255687168637." 
			recipient_list = []
			recipient_list.append(Collaborator.e_mail)
			from_email = 'no-reply@project.org'
			send_mail(subject,message,from_email,recipient_list,fail_silently=False)
						
			message = "Hi, "+user.name+"\nYou have successfully add "+Collaborator.name+" as collaborator on "+project.title+" project" + "by " +user.name + "\n\nRegard,\nIMS developer,\nJoseph Chingalo,\nSoftware Consultant at Unyayo Systems Limited,\nMobile Number: +255687168637."
			recipient_list = []
			recipient_list.append(user.e_mail)
			from_email = 'no-reply@project.org'
			send_mail(subject,message,from_email,recipient_list,fail_silently=False)
			
			
			nameList = user.name.split(" ")	
			userName = 	nameList[0]
			
			projectOwner = project.project_owner
			assignmentList = Project_assignment.objects.filter(project = project)
			memberList = []
			
			for assignment in assignmentList:
				memberList.append(assignment.project_member)
			
			context = {'user':user,'memberList':memberList,'projectOwner':projectOwner,'userName':userName,'contents':'singleproject','project':project}
			return render(request, 'userFunction.html',context)		
			
		else:	
			
			
			context = {'user':user,'userName':userName,'contents':'addCollaborator','project':project,'userList':userList}
			return render(request, 'userFunction.html',context)







#view all issues
def allIssues(request,user_id):
	user = Users.objects.get(id = user_id)

	#checking if current user has login first
	if user.login_status =='log_out':
		users = Users.objects.all()
		userList = []
		for user in users:
			userList.append(user.e_mail)
		userEmailData = json.dumps(userList)
		
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue,'userEmailData':userEmailData}	
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
		users = Users.objects.all()
		userList = []
		for user in users:
			userList.append(user.e_mail)
		userEmailData = json.dumps(userList)
		
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue,'userEmailData':userEmailData}	
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
		users = Users.objects.all()
		userList = []
		for user in users:
			userList.append(user.e_mail)
		userEmailData = json.dumps(userList)
		
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue,'userEmailData':userEmailData}	
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
		users = Users.objects.all()
		userList = []
		for user in users:
			userList.append(user.e_mail)
		userEmailData = json.dumps(userList)
		
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue,'userEmailData':userEmailData}	
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
			asignedUser = Users.objects.get(name = assignee[0])
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
			newAssignment.assignee = asignedUser
			newAssignment.issue = newIssue
			newAssignment.save()
			
			
			#send email after create and assign issue
			subject = "ISSUE CREATION ON "+ newIssue.title + " IN IMS"
			message = "Hi, "+user.name+ "\nYou have successful created \"" + newIssue.title + "\" issue and assigned to "+ asignedUser.name +" on "+project.title +" project in IMS" +"\n\nRegard,\nIMS developer,\nJoseph Chingalo,\nSoftware Consultant at Unyayo Systems Limited,\nMobile Number: +255687168637."
			recipient_list = []
			recipient_list.append(user.e_mail)
			from_email = 'no-reply@project.org'
			send_mail(subject,message,from_email,recipient_list,fail_silently=False)
			
			message = "Hi , " +asignedUser.name+ "\nYou have assigned to \" "+ newIssue.title+ " \"issue on "+project.title +" project in IMS" + "\n\nRegard,\nIMS developer,\nJoseph Chingalo,\nSoftware Consultant at Unyayo Systems Limited,\nMobile Number: +255687168637."
			recipient_list = []
			recipient_list.append(asignedUser.e_mail)
			from_email = 'no-reply@project.org'
			send_mail(subject,message,from_email,recipient_list,fail_silently=False)
			
			
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
		users = Users.objects.all()
		userList = []
		for user in users:
			userList.append(user.e_mail)
		userEmailData = json.dumps(userList)
		
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue,'userEmailData':userEmailData}	
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
		users = Users.objects.all()
		userList = []
		for user in users:
			userList.append(user.e_mail)
		userEmailData = json.dumps(userList)
		
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue,'userEmailData':userEmailData}	
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
		
		assigner = issue.assigner
		assigneeAss = Issue_assignment.objects.get(issue = issue)
		assignee = assigneeAss.assignee	
		
		#send email after comment on the isssue
		subject = "COMMENT ON "+ issue.title + "IN IMS"
		from_email = 'no-reply@project.org'
		if(assigner == user):
			message = "Hi, "+assignee.name+"\n"+user.name +" has commented on \""+issue.title +"\" as \""+commentToIssue.description+"\"" + "\n\nRegard,\nIMS developer,\nJoseph Chingalo,\nSoftware Consultant at Unyayo Systems Limited,\nMobile Number: +255687168637."
			recipient_list = []	
			recipient_list.append(assignee.e_mail)	
			send_mail(subject,message,from_email,recipient_list,fail_silently=False)
		else:
			message = "Hi, "+assigner.name+"\n"+user.name +" has commented on \""+issue.title +"\" as \""+commentToIssue.description+"\"" + "\n\nRegard,\nIMS developer,\nJoseph Chingalo,\nSoftware Consultant at Unyayo Systems Limited,\nMobile Number: +255687168637."
			recipient_list = []	
			recipient_list.append(assigner.e_mail)	
			send_mail(subject,message,from_email,recipient_list,fail_silently=False)
			
			
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
		users = Users.objects.all()
		userList = []
		for user in users:
			userList.append(user.e_mail)
		userEmailData = json.dumps(userList)
		
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue,'userEmailData':userEmailData}	
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
			previousStatus = status_log[numberOfStatus - 1].status
			
			statusChange = Issue_status()
			statusChange.status_changer = user
			statusChange.issue = issue
			statusChange.status = "close"	
			statusChange.save()
			#send email after close an issue:
			subject = "STATUS CHANGES ON \""+issue.title +"\" issue  IN IMS"
						
			assigner = issue.assigner
			assigneeAss = Issue_assignment.objects.get(issue = issue)
			assignee = assigneeAss.assignee		
					
			if(user == assigner):
				message = "Hi, " +assignee.name+"\n"+user.name+ " has changed status on "+issue.title +" from "+ previousStatus +" to " + statusChange.status + "\n\nRegard,\nIMS developer,\nJoseph Chingalo,\nSoftware Consultant at Unyayo Systems Limited,\nMobile Number: +255687168637."
				recipient_list = []
				recipient_list.append(assignee.e_mail)
				from_email = 'no-reply@project.org'
				send_mail(subject,message,from_email,recipient_list,fail_silently=False)
			else:
				message = "Hi, " +assigner.name+"\n"+user.name+ " has changed status on "+issue.title +" from "+ previousStatus +" to " + statusChange.status + "\n\nRegard,\nIMS developer,\nJoseph Chingalo,\nSoftware Consultant at Unyayo Systems Limited,\nMobile Number: +255687168637."
				recipient_list = []
				recipient_list.append(assigner.e_mail)
				from_email = 'no-reply@project.org'
				send_mail(subject,message,from_email,recipient_list,fail_silently=False)
			
			
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
		users = Users.objects.all()
		userList = []
		for user in users:
			userList.append(user.e_mail)
		userEmailData = json.dumps(userList)
		
		word = 'You have not login in the system, please login first!'
		captureValue = randrange(100000,999999)	
		context = {'word':word,'captureValue':captureValue,'userEmailData':userEmailData}	
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
		if(status_log[numberOfStatus - 1].status == "close"):
			previousStatus = status_log[numberOfStatus - 1].status
			#change status of issue
			statusChange = Issue_status()
			statusChange.status_changer = user
			statusChange.issue = issue
			statusChange.status = "reopen"	
			statusChange.save()
			
			#send email upon reopen an issue
			subject = "STATUS CHANGES ON \"" + issue.title + "\" issue IN IMS" 
						
			assigner = issue.assigner
			assigneeAss = Issue_assignment.objects.get(issue = issue)
			assignee = assigneeAss.assignee		
					
			if(user == assigner):
				message = "Hi, " +assignee.name+"\n"+user.name+ " has changed status on "+issue.title +" from "+ previousStatus +" to " + statusChange.status + "\n\nRegard,\nIMS developer,\nJoseph Chingalo,\nSoftware Consultant at Unyayo Systems Limited,\nMobile Number: +255687168637."
				recipient_list = []
				recipient_list.append(assignee.e_mail)
				from_email = 'no-reply@project.org'
				send_mail(subject,message,from_email,recipient_list,fail_silently=False)
			else:
				message = "Hi, " +assigner.name+"\n"+user.name+ " has changed status on "+issue.title +" from "+ previousStatus +" to " + statusChange.status + "\n\nRegard,\nIMS developer,\nJoseph Chingalo,\nSoftware Consultant at Unyayo Systems Limited,\nMobile Number: +255687168637."
				recipient_list = []
				recipient_list.append(assigner.e_mail)
				from_email = 'no-reply@project.org'
				send_mail(subject,message,from_email,recipient_list,fail_silently=False)
			
			
			
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







