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
	
#processing login processs
def login(request):
	
	userFromSystem = Users.objects.all()
	word = ''	
	
	if request.POST:
		#taking values from form		
		form = request.POST		
		emailListPosted = form.getlist('email')
		passwordPosted = form.getlist('password')
		p = 'hello statrting login process'
		
		details = emailListPosted[0] + " " + passwordPosted[0]
		
		#check if login user is registered
		for user in userFromSystem:
			if user.e_mail == emailListPosted[0] and user.password == passwordPosted[0]:
				#for registered user				
				word = 'successfully login in the system'
				context = {'m':p,'form':word,'details':details,}
				return render(request,'userFunction.html',context)
			
	#for not registered users
		word = 'Fail to login, either try to login again if you are registered user or signup for new user'		
		context = {'word':word,'details':details,}
		return render(request,'index.html',context)
	








