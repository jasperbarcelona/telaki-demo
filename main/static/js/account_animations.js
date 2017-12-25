$(document).ready(function(){

$('#profile-options').hide();
$('.add-admin-footer-left').hide();

$('.form-control').floatlabel({
    labelEndTop:'-2px'
});

$('#add-admin-modal').on('shown.bs.modal', function () {
    $('#add_admin_first_name').focus();
});

$('#is-super-admin-label').on('click', function () {
    if ($('#is_super_admin').is(":checked")){
        $('#is_super_admin').prop('checked',false);
    }
    else{
        $('#is_super_admin').prop('checked',true);
    }
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

$('#add-admin-modal .add-admin-modal-body .form-control').on('change', function () {
    var re = /[A-Za-z]+$/;
    if (($('#add_admin_last_name').val() != "") && ($('#add_admin_first_name').val() != "") && ($('#add_admin_email').val() != "") && 
        (re.test($('#add_admin_last_name').val())) && 
        (re.test($('#add_admin_first_name').val())) ){
        $('#save-admin').removeAttr('disabled');
    }
    else{
        $('#save-admin').attr('disabled',true);
    }
});

$('#add-admin-modal .add-admin-modal-body .form-control').on('keyup', function () {
    var re = /[A-Za-z]+$/;
    if (($('#add_admin_last_name').val() != "") && ($('#add_admin_first_name').val() != "") && ($('#add_admin_email').val() != "") && 
        (re.test($('#add_admin_last_name').val())) && 
        (re.test($('#add_admin_first_name').val())) ){
        $('#save-admin').removeAttr('disabled');
    }
    else{
        $('#save-admin').attr('disabled',true);
    }
});

$('.add-admin-modal-body .form-control').on('keyup', function (e) {
    var key = e.which;
    if((key == 13) && ($('#save-admin').is(':disabled') == false)){
    	save_admin();
        return false;
    }
});

$('#add-admin-modal').on('hidden.bs.modal', function () {
    $('#add_admin_email').val('');
    $('#add_admin_first_name').val('');
    $('#add_admin_last_name').val('');
    $('.add-admin-modal-body .form-control').change();
    $('#save-admin').attr('disabled',true);
});

});