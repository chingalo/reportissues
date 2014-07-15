

//validation of form on submit if all required fields have been filled
function validateForm(){
	for(var i = 0;i < myform.elements.length;i++){	
		if(myform.elements[i].className == "required" && myform.elements[i].value.length == 0){			
			alert('Fail to create new account, please make sure you fill required fields '+email);
			return false;			
			}		
		}
	
		
	
	}

//e-mail validation on the form
function chechEmail(){
	var email = document.getElementById('email').value;
	var atpos = email.indexOf('@');
	var atdot = email.lastIndexOf('.');
	
	if(atpos < 1 || atdot < atpos+2 || atdot+2 >= email.length){
		alert('incorrect email');
		}	
	}
