/*================================================================================
	Item Name: Materialize - Material Design Admin Template
	Version: 3.1
	Author: GeeksLabs
	Author URL: http://www.themeforest.net/user/geekslabs
================================================================================

NOTE:
------
PLACE HERE YOUR OWN JS CODES AND IF NEEDED.
WE WILL RELEASE FUTURE UPDATES SO IN ORDER TO NOT OVERWRITE YOUR CUSTOM SCRIPT IT'S BETTER LIKE THIS. */
$(function() {

	var start_time = 1420070400;
	var end_time = 1474763510;
	var step = 604800; // 1 week in seconds

	$("#example_id").ionRangeSlider({
		'type': 'double',
		'min': start_time,
		'max': end_time,
		'from': start_time,
		'to': end_time,
		'step': step,
		'grid_snap': true,
		'prettify': function(num) {
			return moment.unix(num).format("MMM DD, YYYY");
		},
	});
	
	$('.button-collapse').sideNav({
		menuWidth: 200,
		edge: 'right',
		closeOnClick: true
	});

	$('#fade_dash.hidden').hide().fadeIn('slow');
});