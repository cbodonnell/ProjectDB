var locButtonClicked = false;

document.getElementById('loc-button').onclick = function() {
	locButtonClicked = true;
	document.getElementById("loc-button").disabled = true;
};

// Escape key function
window.onkeydown = function(event) {
	if (locButtonClicked) {
		if (event.keyCode == 27) {
					document.getElementById("lat-text").value = "";
					document.getElementById("lng-text").value = "";
					document.getElementById("loc-button").disabled = false;
					locButtonClicked = false;
		}
	}
}