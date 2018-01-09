var locButtonClicked = false;
var numFiles = 1;

// Letters and numbers only in project name (for filing purposes)
$('#inputName').keypress(function (e) {
	var txt = String.fromCharCode(e.which);
	if (!txt.match(/[A-Za-z0-9&._- ]/)) {
		return false;
	}
});

// Coordinates button
document.getElementById('loc-button').onclick = function() {
	locButtonClicked = true;
	document.getElementById("loc-button").disabled = true;
};

// File field button
document.getElementById('file-button').onclick = function() {
	numFiles += 1;
	$("#file-field").append("<div><input type='file' name='file-" + numFiles + "'></div>");
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