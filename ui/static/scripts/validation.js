function validateFileSelection() {
	var filename = document.getElementById("file_upload").files[0].name;
	var file = document.getElementById("file_upload").files[0];
	var valid = true;

	var reader = new FileReader();
	reader.onload = function() {
		reader.result.split("\n").forEach(function(line, index, arr) {
			if ((line.split(',').length != 2) && (line != "")) {
				console.log("invalidated: " + line);
				document.getElementById("file_selection").innerHTML = "Selected file is invalid";
				document.getElementById("upload_input_box").style.backgroundColor = "Salmon";
				document.getElementById("file_upload").files[0] = null;
			}
		});
	}
	reader.readAsText(file);

	document.getElementById("upload_input_box").style.backgroundColor = "LightGrey";
	document.getElementById("file_selection").innerHTML = "File selected: " + filename;
};
