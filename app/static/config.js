/* =======================================================================================
 * Copyright 2014 Matt Clyde, Shawn Forgie, Blake Wellington
 * Licensed under GPL v2 (https://github.com/mclyde/HousePlantMonitor/blob/master/LICENSE)
 * ===================================================================================== */


function startMonitoring() {
	$("#startbutton").prop("disabled", true);
	$("#stopbutton").prop("disabled", true);
	$("#startbutton").button('loading');
	$.get('/startMonitoring', function() {
	})
	.done(function() {
	})
	.fail(function() { 
		alert("monitors could not be started!");
	})
	.always(function() {
		$("#startbutton").button('reset');
		$("#startbutton").prop("disabled", false);
		$("#stopbutton").prop("disabled", false);
	});
}

function stopMonitoring() {
	$("#startbutton").prop("disabled", true);
	$("#stopbutton").prop("disabled", true);
	$("#stopbutton").button('loading');
	$.get('/stopMonitoring', function() {
	})
	.done(function() {
	})
	.fail(function() { 
		alert("monitors could not be stopped!");
	})
	.always(function() {
		$("#stopbutton").button('reset');
		$("#startbutton").prop("disabled", false);
		$("#stopbutton").prop("disabled", false);
	});
}