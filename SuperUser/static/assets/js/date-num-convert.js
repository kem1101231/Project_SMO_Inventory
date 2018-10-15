function datenumconvert(input) {
	var dateInput = input.split('-')

	var dateOutput = ''

	switch(dateInput[1]){
		case '1':
			dateOutput = 'Jan. '+dateInput[2]+', '+dateInput[0]
	}
	switch(dateInput[1]){
		case '2':
			dateOutput = 'Feb. '+dateInput[2]+', '+dateInput[0]
	}
	switch(dateInput[1]){
		case '3':
			dateOutput = 'Mar. '+dateInput[2]+', '+dateInput[0]
	}
	switch(dateInput[1]){
		case '4':
			dateOutput = 'Apr. '+dateInput[2]+', '+dateInput[0]
	}
	switch(dateInput[1]){
		case '5':
			dateOutput = 'May '+dateInput[2]+', '+dateInput[0]
	}
	switch(dateInput[1]){
		case '6':
			dateOutput = 'Jun. '+dateInput[2]+', '+dateInput[0]
	}
	switch(dateInput[1]){
		case '7':
			dateOutput = 'Jul. '+dateInput[2]+', '+dateInput[0]
	}
	switch(dateInput[1]){
		case '8':
			dateOutput = 'Aug. '+dateInput[2]+', '+dateInput[0]
	}
	switch(dateInput[1]){
		case '9':
			dateOutput = 'Sep. '+dateInput[2]+', '+dateInput[0]
	}
	switch(dateInput[1]){
		case '10':
			dateOutput = 'Oct. '+dateInput[2]+', '+dateInput[0]
	}
	switch(dateInput[1]){
		case '11':
			dateOutput = 'Nov. '+dateInput[2]+', '+dateInput[0]
	}
	switch(dateInput[1]){
		case '12':
			dateOutput = 'Dec. '+dateInput[2]+', '+dateInput[0]
	}

	return dateOutput

}