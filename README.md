project management system
==========================
It aim on project management on any project.
Its capabilities are :
	
	login for registered users, 
	sign up for new user,
	validate for all required fields before submitttion of signup form,
	checking for correct email,
	list all projects concerned him or her,
	list all issues for a given user,
	create new project,
	add collaboration for a given project,
	create issue on a project and assign to user,
	comment on issue,
	change status like new, close and reopen,
	send e-mail during signup,activation of account, creation of new project or issue,assignment of issue, status change and comment on issue.


How to install this site:
====================================
Install virtualenv on your machine and use it to maintain the site.
The following are couple of commands for operating under virtual env:

	#Install python virtualenv
	$ sudo apt-get install python-virtualenv
	
	#Create a virtual environment directory
	$ virtualenv /path/to/virtualenv_dir
	
	#Activating virtual environment(while you're in virtualenv_dir)
	$ source bin/activate
	
	#Deactivating virtual env
	$ deactivate

After creating and activating virtualenv, while inside virtualenv folder,
clone this site's source codes:
	
	$ https://github.com/chingalo/issuesmanagementsystem.git
	or
	$ https://chingalo@bitbucket.org/chingalo/issue-management-sytem.git

Inside reportissues directory, install project dependencies inside: requirements.txt
	
	$ cd reportissues
	$ pip install -r requirements.txt
Add database  configurations inside reportissues/settings.py, your
database configurations should look something similar to this if you are using MySQL:
	
	DATABASES = {
    'default': { 
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'DATABASE NAME',                     
        'USER': 'USER NAME',
        'PASSWORD': 'PASSWORD',
    }
}
After configuration sync database( run command: python manage.py syncdb) and then run the server( run command: python manage.py runserver ).
Incase of any difficulties in configuration refer to [Django CMS Documentation](http://django-cms.readthedocs.org/en/2.2/getting_started/installation.html)
for more information.

