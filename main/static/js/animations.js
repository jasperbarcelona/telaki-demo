$(document).ready(function(){

$(window).load(function(){
  setTimeout(function() {
    $('#mainPreloader').fadeOut();
  }, 3000);
});

profile_options = 'closed'

$('#profile-options').hide();
$('#replyError').hide();
$('#replySuccess').hide();

$('.form-control.floatlabel').floatlabel({
    labelEndTop:'-2px'
});

$(".datepicker").datepicker({
    dateFormat: "MM dd, yy"
});


$('#user-icon-container').on('click', function () {
    var $this = jQuery(this);
    if ($this.data('activated')) return false;  // Pending, return
    $this.data('activated', true);
    setTimeout(function() {
      $this.data('activated', false)
    }, 500); // Freeze for 500ms

    if ((typeof profile_options === 'undefined') || (profile_options == 'closed')){
        var travel_width = $('#profile-options').width();
        $('#user-icon-container').animate({'margin-right':travel_width+2});
        profile_options = 'open'
        setTimeout(function() {
            $('#profile-options').fadeIn();
        }, 500); // Freeze for 500ms
    }
    else{
        $('#profile-options').fadeOut();
        profile_options = 'closed'
        setTimeout(function() {
            $('#user-icon-container').animate({'margin-right':'0'});
        }, 500); // Freeze for 500ms
    }
});

$('#composeMessage').on('click', function (e) {
    $('#messageContainer').show();
    $('#messageContainer').removeClass('minimized');
    $('#messageBody').focus();
});

$('#minimizeMessage').on('click', function (e) {
    $('#messageContainer').addClass('minimized');
});

$('#closeMessage').on('click', function (e) {
    $('#messageContainer').hide();
    initialize_recipients();
});

(function() {
  $('.message-header div').on('click', function(e){
    if (e.target == this){
      $('#messageContainer').toggleClass('minimized');
    }
  });
})();

(function() {
  $('.contact-type-picker').on('click', function(e){
    $(this).toggleClass('selected');
  });
})();

(function() {
  $('.group-picker').on('click', function(e){
    $(this).toggleClass('selected');
  });
})();

(function() {
  $('#closeReplyError').on('click', function(e){
    $('#replyError').fadeOut();
  });
})();

(function() {
  $('#closeReplySuccess').on('click', function(e){
    $('#replySuccess').fadeOut();
  });
})();

$('#createGroupModal').on('shown.bs.modal', function () {
    $('#addGroupName').focus();
});

$('#addContactModal').on('shown.bs.modal', function () {
    $('#addContactName').focus();
});

$('#saveContactModal').on('hidden.bs.modal', function () {
  $('#saveContactModal .form-control').val('');
  $('#saveContactModal .contact-type-picker.selected').removeClass('selected');
  $('#saveContactModal .group-picker.selected').removeClass('selected');
  setTimeout(function() {
    $('#saveContactBtn').attr('disabled', true);
    }, 500);
});






svg = $('#loaderSVG').drawsvg({
  callback: function() {
    animate();
  }
});

function animate() {
  svg.drawsvg('animate');  
}

animate();


});