function validateForm(){
	for(var i = 0;i < myform.elements.length;i++){
		if(myform.elements[i].className == "required" && myform.elements[i].value.length == 0){			
			alert('Fail to create new account, please make sure you fill required fields');
			return false;			
			}		
		}
	}


