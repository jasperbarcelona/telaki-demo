function show_form(){
	$('#page1-pic-container').animate({'left':'110%'});
	$('#demo-form-container').delay(1000).animate({'left':'0'});
}

function hide_form(){
	$('#demo-form-container').animate({'left':'100%'});
	$('#page1-pic-container').delay(1000).animate({'left':'0'});
}