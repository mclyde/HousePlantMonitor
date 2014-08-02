/* =======================================================================================
 * Copyright 2014 Matt Clyde, Shawn Forgie, Blake Wellington
 * Licensed under GPL v2 (https://github.com/mclyde/HousePlantMonitor/blob/master/LICENSE)
 * ===================================================================================== */

$(document).ready(function() { $('body').hide().fadeIn(1000); })

var popContent = "<form><input type='text'/></form>";

$(function () { 
    $("[data-toggle='popover']").popover({	container:'body',
    										html:'true',
    										placement:'bottom',
    										trigger:'focus',
    										content:popContent
    									}); 
});
