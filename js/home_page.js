//function to run when the page is nice and loaded
window.onload = function() {

	//get our from element that sends new movie trailer data
	var form = document.new_trailer_data;

	//add a jquery submit function to do some sanity checks on the input
	//its very easy to look at the html code using dev tools and remove the required 
	//attributes from the input fields
	$(form).submit(function() {
		
		//store out input values in a list
		var input_boxes = [
			this.title,
			this.poster_image_link,
			this.youtube_trailer_link
		];

		//any inputs that need to be checked we can place them in here
		//so the user knows what to be corrected
		inputs_need_correction = [];

		//loop through the list of values and if isEmpty(value), 
		//we append that input boxes placeholder to a list that needs to be corrected to a list
		//I am using the placeholder to specify what input box needs to be corrected
		each(input_boxes, function(ci) {
			if (isEmpty(ci.value)) {
				inputs_need_correction.push(ci.placeholder)
			}
		});

		//if we have inputs that need to be corrected
		//we call creatError and pass in the inputs_need_correction array
		console.log(inputs_need_correction)
		if (inputs_need_correction.length > 0) {
			createErr(inputs_need_correction);
		}
		return false
		
		
	})
	
}

//declare function isEmpty takes in a string 
//returns true if empty string
function isEmpty(strang) {
	return strang == "";
}
function each(data, funky_town) {
	for (var i = 0; i < data.length; i++) {
		funky_town(data[i]);
	}
}
function createErr(user_input_errors) {
	//get the div with the id of form_err
	//set its display to visible so the browser will include it in the dom
	//loop through our user_input_erros and for each error (placeholder)
	//we add that error to the innerHTML of our error div

	var err_div = document.getElementById("form_error");
	console.log(err_div);
	err_div.style.display = "inline";

	err_div.innerHTML += "<h3>The Following fields need to be corrected</h3>";
	each(user_input_errors, function(e) {
		err_div.innerHTML += "<p>" + e + "</p>";
	})
}