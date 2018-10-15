
function display(form){
			if (form.unmField.value=="root") { 
				if (form.passField.value=="root") {              
						location="/requisitioner" 
				} else {
						alert("Invalid Password")
					    }
			} else {  
				alert("Invalid Username")
					}
		}


function doLogin(form){
		
		var uname = form.unmField.value;
		var password = form.passField.value;

		var accttype = getAcctPrev(uname, password)

		if (accttype == "Wrong Password") {
			alert("Wrong Password");
		}

		else{

			
			if (accttype == "requisitioner") {
				location = "/requisitioner";
			}

			if (accttype == "smoadmin") {
				location = "/inventory_office";			
			}

			if (accttype == "procadmin") {
        		location = "/procurement_office";
      		}
		}
}


function getAcctPrev(uname, password){
		
		if (uname == "requi") {

			if (password == "pass") {
				return "requisitioner";
			} else {
				return "Wrong password";
			}
			
		}

		if (uname == "smoadmin") {
			
			if (password == "pass") {
				return "smoadmin";
			} else {
				return "Wrong password";
			}
			
		}


		if (uname == "smorecei") {
			
			if (password == "pass") {
				return "smoreceive";
			} else {
				return "Wrong password";
			}
			
		}

		if (uname == "smoinven") {
			
			if (password == "pass") {
				return "smoinven";
			} else {
				return "Wrong password";
			}
			
		}

		if (uname == "smoacct") {
			
			if (password == "pass") {
				return "smoacctmgr";
			} else {
				return "Wrong password";
			}
		}

		if (uname == "apprvcaf") {
			
			if (password == "pass") {
				return "vcaf";
			} else {
				return "Wrong password";
			}
			
		}

		if (uname == "apprchan") {
			
			if (password == "pass") {
				return "chancellor";
			} else {
				return "Wrong password";
			}
		}

		if (uname == "apprchan") {
			return "chancellor";
		}

		if (uname == "procadmin") {
			
			if (password == "pass") {
				return "procadmin";
			} else {
				return "Wrong password";
			}
		}

		if (uname == "procclerk") {
			
			if (password == "pass") {
				return "procclerk";
			} else {
				return "Wrong password";
			}	
		}
}