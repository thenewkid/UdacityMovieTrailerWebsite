//function to run when the page is nice and loaded
window.onload = function() {

	//declare our input boxes
	var input_boxes = [
		document.getElementById("title"),
		document.getElementById("poster_image_link"),
		document.getElementById("youtube_trailer_link")
	];


	//call our assignInputs on the input_box list
	assignInputs(input_boxes);

	//add a jquery submit function to do some sanity checks on the input
	//its very easy to look at the html code using dev tools and remove the required 
	//attributes from the input fields, thus allowing somebody to send bad data to the server
	$("#submit_button").click(function() {

		//any inputs that need to be checked we can place them in here
		//so the user knows what to be corrected
		inputs_need_correction = [];

		//loop through the list of input_box_values and if isEmpty(value), 
		//we append that input boxes placeholder to a list that needs to be corrected to a list
		//I am using the placeholder to specify what input box needs to be corrected
		each(input_boxes, function(ci) {
			if (isEmpty(ci.value)) {
				inputs_need_correction.push(ci.placeholder)
			}
			//while were here looping through our inputs
			//we will add an oninput function called checkNotEmpty
		});

		//if we have inputs that need to be corrected
		//we call creatError and pass in the inputs_need_correction array
		if (inputs_need_correction.length > 0) {
			createErr(inputs_need_correction);
		}
		else {
			$.ajax({
				url: document.URL,
				data: {
					"title": input_boxes[0].value,
					"poster_image_link": input_boxes[1].value,
					"youtube_trailer_link": input_boxes[2].value
				},
				type: "POST",
				dataType: "json",
				success: function(returned_html) {
					if (returned_html == "reload") {
						reloadPage();
					}
					else if (returned_html == "exists") {
						alert("That title already exists");
					}
				}
			})
		}
	})

	
}

//declare function isEmpty takes in a string 
//returns true if empty string

function reloadPage() {
	var chill = window.location;
	window.location = chill.protocol + '//' + chill.host + chill.pathname;
}
function isEmpty(strang) {
	return strang == "";
}
function each(data, funky_town) {
	for (var i = 0; i < data.length; i++) {
		funky_town(data[i]);
	}
}
function checkNotEmpty() {
	if (this.value.length > 0)
		assignClass(this, "border-blue")
	else {
		if ($(this).hasClass("border-blue")) 
			$(this).removeClass("border-blue")
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

	err_div.innerHTML = ""
	err_div.innerHTML += "<h3>The Following fields need to be corrected</h3>";
	each(user_input_errors, function(e) {
		err_div.innerHTML += "<p class='err_msg lead'>" + e + "</p>";
	})
}
//takes in a element and a class name (bootstrap class name)
//uses the jquery addClass() function to assign the class
function assignClass(html_element, classname) {
	$(html_element).addClass(classname);
}

//this function takes in a list of input elements
//assigns each input an oninput function
function assignInputs(input_list) {
	each(input_list, function(e) {
		e.oninput = checkNotEmpty;
	})
}