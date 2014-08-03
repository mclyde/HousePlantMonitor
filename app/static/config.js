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

$(function () {
	$('body').hide().fadeIn(1000);
    $("[data-toggle='popover']").popover({	container:'body',
    										html:'true',
    										placement:'bottom',
    										trigger:'click',
    										title: function() {
												return $('#popover-head').html();
											},
											content: function() {
												return $('#popover-content').html();
											}
    									});
});

$(document).on('change', 'select.deviceClass', function() {
	var key = $(this).val();
	console.log(key);
	switch(key) {
		case 'inputs':
			list(inputs);
			break;
		case 'outputs':
			list(outputs);
			break;
		default:
			break;
	}
});

function list(arr) {
	$('.subset').html("");
	$(arr).each(function(i) {
		$('.subset').append("<option value=\"" + arr[i].value + "\">" + arr[i].display + "</option>");
	});
}




