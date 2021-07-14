function check_analysis() {
	const download_box = document.getElementById('analyzer_results')
	const result_message = document.getElementById('analyzer_message')

	get_status(download_box, result_message, 'check_analyzer')
};

function check_search() {
	const download_box = document.getElementById('explorer_results')
	const result_message = document.getElementById('explorer_message')

	get_status(download_box, result_message, 'check_explorer')
};

function get_status(box, text, source) {
	const base_url = window.location.toString().slice( 0, window.location.toString().indexOf('&') );

	fetch(base_url + "/" + source)
		.then(response => response.json())
		.then(json_data => {
			console.log(json_data)
			if (json_data.state == "running") {
				box.style.backgroundColor = "Yellow"
				text.innerHTML = "Processing"
			} else if (json_data.state == "stopped") {
				if ("result" in json_data) {
					if (json_data.result == 0) {
						box.style.backgroundColor = "LightGreen"
						text.innerHTML = "Finished"
					} else {
						box.style.backgroundColor = "Salmon"
						text.innerHTML = "Error"
					}
				} else {
					box.style.backgroundColor = "White"
				}
			}
		});
};

analysis = setInterval(check_analysis, 2*1000)
search = setInterval(check_search, 2*1000)
