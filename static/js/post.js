$(document).ready(function() {    
    $('#blogpage').ready(function(){
		var windowHeight = $(window).height();
		var targetHeight = windowHeight-40;
		//alert(targetHeight);
		$('#blogpage').css('height',targetHeight);
	});
 });
 
 $(window).resize(function() {    
    $('#blogpage').ready(function(){
		var windowHeight = $(window).height();
		var targetHeight = windowHeight-40;
		//alert(targetHeight);
		$('#blogpage').css('height',targetHeight);
	});
 });