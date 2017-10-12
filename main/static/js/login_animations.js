$(document).ready(function(){

$('#login-error-container').hide();

setTimeout(function(){
    $("#school_no").focus();
}, 0);

$(window).load(function() {
    $('#user_email').focus();
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
