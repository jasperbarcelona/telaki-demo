$(document).ready(function(){

$('#login-error-container').hide();

$(window).load(function() {
	$("#client_no").focus();
    $('#login-intro').hide();
});

$('#login-form .form-control').floatlabel({
    labelEndTop:'-2px'
});

$('#login-form').on('submit', function(e){
      e.preventDefault();
      login();
  });

})
