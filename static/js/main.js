var locButtonClicked = false;
var numFiles = 1;
var numUses = 1;

$(".new-entry-button").click(function () {
	$content = $(".new-entry");
	//open up the content needed - toggle the slide
	//if visible, slide up, if not slidedown.
    $content.slideToggle(500, function () {
    });
});

// Letters and numbers only in project name (for filing purposes)
$('#inputName').keypress(function (e) {
	var txt = String.fromCharCode(e.which);
	if (!txt.match(/[A-Za-z0-9&._- ]/)) {
		return false;
	}
});

// Land use selection
function showfield(name){
	if(name=='Other') {
		document.getElementById('other ' + numUses.toString()).innerHTML='Other: \
		<input type="text" name="other" />';
	}
	else {
		document.getElementById('other ' + numUses.toString()).innerHTML='';
	}
}

// Numbers only in location fields
$('#lat-text').keypress(function (e) {
	var txt = String.fromCharCode(e.which);
	if (!txt.match(/[0-9.]/)) {
		return false;
	}
});

$('#lng-text').keypress(function (e) {
	var txt = String.fromCharCode(e.which);
	if (!txt.match(/[0-9.-]/)) {
		return false;
	}
});

// Coordinates button
document.getElementById('loc-button').onclick = function() {
	locButtonClicked = true;
	document.getElementById("loc-button").disabled = true;
};

// Land use field button
document.getElementById('use-button').onclick = function() {
	numUses += 1;
	$("#use-field").append(
	"<select name='uses' id='lane-use-selection' \
	onchange='showfield(this.options[this.selectedIndex].value)'>\
	<option selected='selected'>Please select ...</option>\
	<option value='Plane'>Plane</option>\
	<option value='Train'>Train</option>\
	<option value='Own Vehicle'>Own Vehicle</option>\
	<option value='Other'>Other</option>\
	</select><div id='other " + numUses + "'></div>");
};

// File field button
document.getElementById('file-button').onclick = function() {
	numFiles += 1;
	$("#file-field").append(
	"<div><input type='file' name='file-" + numFiles + "'></div>");
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