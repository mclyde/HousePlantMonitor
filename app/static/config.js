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
	{display:'Email', value:'email'},
	{display:'Text Message', value:'text'},
	{display:'Tweet', value:'tweet'},
	{display:'Motor: Shades', value:'shade'},
	{display:'Motor: Water', value:'water'}
];
var defaults = [
	{display:'---', value:''}
]
var sliderOptions = {
	range:true,
	min: 0,
	max: 1023,
	step: 1,
	tooltip: 'hide',
	value: [0, 1023]
};

$(function () {
	$('body').hide().fadeIn(1000);
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
			$('#submitbutton').show();
			break;
		case 'defaults':
			list(defaults);
			$('#inputMode').hide();
			$('#outputMode').hide();
			$('#submitbutton').hide();
			break;
	}
});

function list(arr) {
	$('.subset').html("");
	$(arr).each(function(i) {
		$('.subset').append("<option value=\"" + arr[i].value + "\">" + arr[i].display + "</option>");
	});
}




