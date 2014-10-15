//SHOW/HIDE MAIN MENU XS
$( "#showmenu" ).click(function() {
  $( "#mainmenu" ).toggle();
});
$( "#showmenuuser" ).click(function() {
  $( "#usermenu" ).toggle();
});

// HOME CHARACTER UPDATE INFO SLIDER
$(".heroupdate").hover(
    function(){
        $(this).find(".caption").filter(':not(:animated)').animate({top:'60px'},{duration :100});     
},
    function() {
        $(this).find(".caption").animate({top:'168px'},{duration:500});
});

// TIMER
var delay = (function(){
  var timer = 0;
  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
  };
})();


// SEARCH
$('#q').keyup(function() {
	
	delay(function(){
	
	if($('input#q').val().length > 1){
		
		$.ajax({
			url: '/search_query.php',
			type: 'get',
			data: {q: $('input#q').val()},
			success: function(response) {
				$('#searchresult').html(response);
				$('#searchresult').parent().css('display', 'block');
			}
		});
	} else {
		$('#searchresult').parent().css('display', 'none');
	}
	
	// scroll searchfield to top
		$('#searchform').animatescroll({scrollSpeed:500,easing:'easeInQuart'});
	
	}, 200 ); // milliseconds delay before doing query
	
});


// Avoid `console` errors in browsers that lack a console.
(function() {
    var method;
    var noop = function () {};
    var methods = [
        'assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error',
        'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log',
        'markTimeline', 'profile', 'profileEnd', 'table', 'time', 'timeEnd',
        'timeStamp', 'trace', 'warn'
    ];
    var length = methods.length;
    var console = (window.console = window.console || {});

    while (length--) {
        method = methods[length];

        // Only stub undefined methods.
        if (!console[method]) {
            console[method] = noop;
        }
    }
}());