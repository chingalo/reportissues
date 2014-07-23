
//validation of form on submit if all required fields have been filled
function validateForm(){
	var test = 0;
	for(var i = 0;i < myform.elements.length;i++){	
		if(myform.elements[i].className == "required" && myform.elements[i].value.length == 0){			
			alert('Fail to create new account, please make sure you fill required fields ');
			return false;			
			}		
		}
		
	for(var i = 0;i < myform.elements.length;i++){	
		if(myform.elements[i].className == "required" && myform.elements[i].value.length != 0 ){			
			test = 1;			
			}		
		}
	var password = document.getElementById('password').value;
	var passwordConf = document.getElementById('passwordConfirmation').value;	
	
	if (password != passwordConf){
		alert('Password does not match...');
		return false;
		}	
	
	var captcha  = document.getElementById('captcha').value;
	var captchaConf  = document.getElementById('captchaConfimation').value;
		
	if(test == 1 && captcha == captchaConf){				
		alert('You have successfull create account ');
		return true;
		}
	else{
		alert('PLease check cature value.....');
		return false;
		}	
		
	}
	


//  validation of new issues creation and assign to user
function createNewIssue(){
	title = document.getElementById('titleOfIssue').value;
	desc = document.getElementById('descriptionOfProject').value;
	if(title == ""){
		alert("Fill the Title of issue....");
		return false;
		}
	
	else{
		if(desc == ""){
			alert("Please decribe issue....");
			return false;
			}
		else{
			alert("You have successfull create new issue");
			return true;
			
			}
		
		}
	
	}




//validation of form on submit if all required fields have been filled
function editProfile(){
	for(var i = 0;i < myform.elements.length;i++){	
		if(myform.elements[i].className == "required" && myform.elements[i].value.length == 0){			
			alert('Fail to edit your account, please make sure you fill required fields ');
			return false;			
			}		
		}
	for(var i = 0;i < myform.elements.length;i++){	
		if(myform.elements[i].className == "required" && myform.elements[i].value.length != 0){			
			alert('You have successfull edit accoint ');
			return true;			
			}		
		}	
		
	}


// comment form validation 
function commentValidation(){
	
	var comment = document.getElementById('comments').value;
	
	if (comment == ""){
		alert("You have not  enter any comment, please enter your comment first before submit");
		return false;		
		}	
	
	}
	
// create new project form validation	

function createProject(){
	var title = document.getElementById('titleOfProject').value;
	var desc = document.getElementById('descriptionOfProject').value;
	
	if(title == ""){
		alert("Please fill the title of project");
		return false;
		}
		
	if(desc == ""){
		alert("Please fill the description of project");
		return false;
		}
	if(title != "" && desc != ""){
		alert("You have successfully create new project !!");
		return true;
		}	
	}	
	

//edit project form validation
function editProject(){
	var title = document.getElementById('titleOfProject').value;
	var desc = document.getElementById('descriptionOfProject').value;
	
	if(title == ""){
		alert("Please fill the title of project");
		return false;
		}
		
	if(desc == ""){
		alert("Please fill the description of project");
		return false;
		}
	if(title != "" && desc != ""){
		alert("You have successfully edit project !!");
		return true;
		}	
	}
	

//e-mail validation on the form
function chechEmailLogin(){
	var email = document.getElementById('emaillogin').value;
	var atpos = email.indexOf('@');
	var atdot = email.lastIndexOf('.');

	if(atpos < 1 || atdot < atpos+2 || atdot+2 >= email.length){
		alert('Incorrect email');
		document.getElementById('emaillogin').focus();
		}	
	}
	
