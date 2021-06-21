function check_analysis() {
	const base_url = window.location.toString().slice( 0, window.location.toString().indexOf('&') );
	const download_box = document.getElementById('download_box')
	const result_message = document.getElementById('result_message')

	fetch(base_url + "/check_status")
		.then(response => response.json())
		.then(json_data => {
			console.log(json_data)
			if (json_data.state == "running") {
				download_box.style.backgroundColor = "Yellow"
				result_message.innerHTML = "Processing"
			} else if (json_data.state == "stopped") {
				if ("result" in json_data) {
					if (json_data.result == 0) {
						download_box.style.backgroundColor = "LightGreen"
						result_message.innerHTML = "Successfully processed"
					} else {
						download_box.style.backgroundColor = "Red"
						result_message.innerHTML = "Error"
					}
				} else {
					download_box.style.backgroundColor = "White"
				}
			}
		});
};

check_analysis()
vvs_status_check = setInterval(check_analysis, 2*1000)
