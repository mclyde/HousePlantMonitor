/* =======================================================================================
 * Copyright 2014 Matt Clyde, Shawn Forgie, Blake Wellington
 * Licensed under GPL v2 (https://github.com/mclyde/HousePlantMonitor/blob/master/LICENSE)
 * ===================================================================================== */

var inputs = [
	{display:'Photometer', value:'light'},
	{display:'Soil Monitor', value:'soil'},
	{display:'Thermometer', value:'temp'}
];
var outputs = [
	//{display:'Email', value:'email'},
	//{display:'Text Message', value:'text'},
	//{display:'Tweet', value:'tweet'},
	{display:'Motor: Shades', value:'shade'},
	{display:'Motor: Water', value:'water'}
];
var defaults = [
	{display:'---', value:''}
]

$(function () {
	$('#inputMode').hide();
	$('#outputMode').hide();
	$('#submitbutton').hide();
});

$(document).on('change', 'select.deviceClass', function() {
	switch($(this).val()) {
		case 'inputs':
			list(inputs);
			$('#outputMode').hide();
			$('#inputMode').show();
			$('#submitbutton').show();
			break;
		case 'outputs':
			list(outputs);
			$('#inputMode').hide();
			$('#outputMode').show();
			$('#delaytrigger').hide();
			$('#submitbutton').show();
			break;
		case 'defaults':
			list(defaults);
			$('#inputMode').hide();
			$('#outputMode').hide();
			$('#pollinginterval').show();
			$('#submitbutton').hide();
			break;
	}
});

$(document).on('change', 'select.subset', function() {
	switch($(this).val()) {
		case 'shade':
			$('#delaytrigger').hide();
			break;
		case 'water':
			$('#delaytrigger').show();
			break;
		case 'defaults':
			break;
	}
});

function list(arr) {
	$('.subset').html("");
	$(arr).each(function(i) {
		$('.subset').append("<option value=\"" + arr[i].value + "\">" + arr[i].display + "</option>");
	});
}