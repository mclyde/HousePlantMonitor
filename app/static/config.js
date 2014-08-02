/* =======================================================================================
 * Copyright 2014 Matt Clyde, Shawn Forgie, Blake Wellington
 * Licensed under GPL v2 (https://github.com/mclyde/HousePlantMonitor/blob/master/LICENSE)
 * ===================================================================================== */

$(document).ready(function() { $('body').hide().fadeIn(1000); });

var deviceTypes = {
	'inputs':  ['Photometer', 'Soil Monitor', 'Thermometer'],
	'outputs': ['Email', 'Text Message', 'Tweet',  'Motor: Shades', 'Motor: Water']
}

var $types = $('select.deviceClass');
var $subset = $('select.subset');
$types.change(function () {
	$subset.empty().append(function() {
		var displayList = '';
		$.each(deviceTypes[$types.val()], function(item) {
			displayList += '<option>' + item + '</option>';
		});
		return displayList;
	});
}).change();

$(function () { 
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

