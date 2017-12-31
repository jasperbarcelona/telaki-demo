/* NAVIGATION */

function show_conversations(slice_from) {
  $('.panel-nav-item').removeClass('active');
  $('#navConversations').addClass('active');
  $.get('/conversations',
  {
    slice_from:slice_from
  },
    function(data){
      $('.content').html(data);
    });
}

function show_blasts(slice_from) {
  $('.panel-nav-item').removeClass('active');
  $('#navBlasts').addClass('active');
  $.get('/blasts',
  {
    slice_from:slice_from
  },
    function(data){
      $('.content').html(data);
    });
}

function show_payment_reminders(slice_from) {
  $('.panel-nav-item').removeClass('active');
  $('#navReminders').addClass('active');
  $.get('/reminders',
  {
    slice_from:slice_from
  },
    function(data){
      $('.content').html(data);
    });
}

function show_contacts(slice_from) {
  $('.panel-nav-item').removeClass('active');
  $('#navContacts').addClass('active');
  $.get('/contacts',
  {
    slice_from:slice_from
  },
    function(data){
      $('.content').html(data);
    });
}

function show_groups(slice_from) {
  $('.panel-nav-item').removeClass('active');
  $('#navGroups').addClass('active');
  $.get('/groups',
  {
    slice_from:slice_from
  },
    function(data){
      $('.content').html(data);
    });
}

/* END OF NAVIGATION */

/* START OF PAGINATION */

function conversation_next_page() {
  $.post('/conversations/next',
    function(data){
      $('#conversations').html(data['template']);
      $('#paginationShowingConversation').html(data['showing']);
      $('#paginationTotalConversation').html(data['total_entries']);
      $('.pagination-btn').blur();

      if (data['prev_btn'] == 'disabled') {
        $('.pagination-btn.left.conversation').attr('disabled', true);
      }
      else {
        $('.pagination-btn.left.conversation').attr('disabled', false);
      }

      if (data['next_btn'] == 'disabled') {
        $('.pagination-btn.right.conversation').attr('disabled', true);
      }
      else {
        $('.pagination-btn.right.conversation').attr('disabled', false);
      }
    });
}

function conversation_prev_page() {
  $.post('/conversations/prev',
    function(data){
      $('#conversations').html(data['template']);
      $('#paginationShowingConversation').html(data['showing']);
      $('#paginationTotalConversation').html(data['total_entries']);
      $('.pagination-btn').blur();

      if (data['prev_btn'] == 'disabled') {
        $('.pagination-btn.left.conversation').attr('disabled', true);
      }
      else {
        $('.pagination-btn.left.conversation').attr('disabled', false);
      }

      if (data['next_btn'] == 'disabled') {
        $('.pagination-btn.right.conversation').attr('disabled', true);
      }
      else {
        $('.pagination-btn.right.conversation').attr('disabled', false);
      }
    });
}

function blast_next_page() {
  $.post('/blasts/next',
    function(data){
      $('#blasts').html(data['template']);
      $('#paginationShowingBlasts').html(data['showing']);
      $('#paginationTotalBlasts').html(data['total_entries']);
      $('.pagination-btn').blur();

      if (data['prev_btn'] == 'disabled') {
        $('.pagination-btn.left.blast').attr('disabled', true);
      }
      else {
        $('.pagination-btn.left.blast').attr('disabled', false);
      }

      if (data['next_btn'] == 'disabled') {
        $('.pagination-btn.right.blast').attr('disabled', true);
      }
      else {
        $('.pagination-btn.right.blast').attr('disabled', false);
      }
    });
}

function blast_prev_page() {
  $.post('/blasts/prev',
    function(data){
      $('#blasts').html(data['template']);
      $('#paginationShowingBlasts').html(data['showing']);
      $('#paginationTotalBlasts').html(data['total_entries']);
      $('.pagination-btn').blur();

      if (data['prev_btn'] == 'disabled') {
        $('.pagination-btn.left.blast').attr('disabled', true);
      }
      else {
        $('.pagination-btn.left.blast').attr('disabled', false);
      }

      if (data['next_btn'] == 'disabled') {
        $('.pagination-btn.right.blast').attr('disabled', true);
      }
      else {
        $('.pagination-btn.right.blast').attr('disabled', false);
      }
    });
}

function reminder_next_page() {
  $.post('/reminders/next',
    function(data){
      $('#reminders').html(data['template']);
      $('#paginationShowingReminders').html(data['showing']);
      $('#paginationTotalReminders').html(data['total_entries']);
      $('.pagination-btn').blur();

      if (data['prev_btn'] == 'disabled') {
        $('.pagination-btn.left.reminder').attr('disabled', true);
      }
      else {
        $('.pagination-btn.left.reminder').attr('disabled', false);
      }

      if (data['next_btn'] == 'disabled') {
        $('.pagination-btn.right.reminder').attr('disabled', true);
      }
      else {
        $('.pagination-btn.right.reminder').attr('disabled', false);
      }
    });
}

function reminder_prev_page() {
  $.post('/reminders/prev',
    function(data){
      $('#reminders').html(data['template']);
      $('#paginationShowingReminders').html(data['showing']);
      $('#paginationTotalReminders').html(data['total_entries']);
      $('.pagination-btn').blur();

      if (data['prev_btn'] == 'disabled') {
        $('.pagination-btn.left.reminder').attr('disabled', true);
      }
      else {
        $('.pagination-btn.left.reminder').attr('disabled', false);
      }

      if (data['next_btn'] == 'disabled') {
        $('.pagination-btn.right.reminder').attr('disabled', true);
      }
      else {
        $('.pagination-btn.right.reminder').attr('disabled', false);
      }
    });
}

function contact_next_page() {
  $.post('/contacts/next',
    function(data){
      $('#contacts').html(data['template']);
      $('#paginationShowingContacts').html(data['showing']);
      $('#paginationTotalContacts').html(data['total_entries']);
      $('.pagination-btn').blur();

      if (data['prev_btn'] == 'disabled') {
        $('.pagination-btn.left.contact').attr('disabled', true);
      }
      else {
        $('.pagination-btn.left.contact').attr('disabled', false);
      }

      if (data['next_btn'] == 'disabled') {
        $('.pagination-btn.right.contact').attr('disabled', true);
      }
      else {
        $('.pagination-btn.right.contact').attr('disabled', false);
      }
    });
}

function contact_prev_page() {
  $.post('/contacts/prev',
    function(data){
      $('#contacts').html(data['template']);
      $('#paginationShowingContacts').html(data['showing']);
      $('#paginationTotalContacts').html(data['total_entries']);
      $('.pagination-btn').blur();

      if (data['prev_btn'] == 'disabled') {
        $('.pagination-btn.left.contact').attr('disabled', true);
      }
      else {
        $('.pagination-btn.left.contact').attr('disabled', false);
      }

      if (data['next_btn'] == 'disabled') {
        $('.pagination-btn.right.contact').attr('disabled', true);
      }
      else {
        $('.pagination-btn.right.contact').attr('disabled', false);
      }
    });
}

function group_next_page() {
  $.post('/groups/next',
    function(data){
      $('#groups').html(data['template']);
      $('#paginationShowingGroups').html(data['showing']);
      $('#paginationTotalGroups').html(data['total_entries']);
      $('.pagination-btn').blur();

      if (data['prev_btn'] == 'disabled') {
        $('.pagination-btn.left.group').attr('disabled', true);
      }
      else {
        $('.pagination-btn.left.group').attr('disabled', false);
      }

      if (data['next_btn'] == 'disabled') {
        $('.pagination-btn.right.group').attr('disabled', true);
      }
      else {
        $('.pagination-btn.right.group').attr('disabled', false);
      }
    });
}

function group_prev_page() {
  $.post('/groups/prev',
    function(data){
      $('#groups').html(data['template']);
      $('#paginationShowingGroups').html(data['showing']);
      $('#paginationTotalGroups').html(data['total_entries']);
      $('.pagination-btn').blur();

      if (data['prev_btn'] == 'disabled') {
        $('.pagination-btn.left.group').attr('disabled', true);
      }
      else {
        $('.pagination-btn.left.group').attr('disabled', false);
      }

      if (data['next_btn'] == 'disabled') {
        $('.pagination-btn.right.group').attr('disabled', true);
      }
      else {
        $('.pagination-btn.right.group').attr('disabled', false);
      }
    });
}

/* END OF PAGINATION */

function textCounter(field,field2,maxlimit){
 var countfield = document.getElementById(field2);
  if( field.value.length > maxlimit ){
    field.value = field.value.substring( 0, maxlimit );
  return false;
  }
  else{
    countfield.value = "Remaining: " + (maxlimit - field.value.length);
  }
}

function replyCounter(field,field2,maxlimit){
 var countfield = document.getElementById(field2);
  if( field.value.length > maxlimit ){
    field.value = field.value.substring( 0, maxlimit );
  return false;
  }
  else{
    countfield.value = "Remaining: " + (maxlimit - field.value.length);
  }
}

function open_conversation(conversation_id) {
  $.get('/conversation',
    {
      conversation_id:conversation_id
    },
    function(data){
      $('.content').html(data);
    });
}

function supply_msisdn(msisdn) {
  $('#saveContactMsisdn').val($('#unsavedMsisdn').html());
  $('#saveContactMsisdn').change();
  setTimeout(function(){
    $('#saveContactName').focus();
  }, 800);
}

function save_contact() {
  $('#saveContactBtn').button('loading');

  var groups = [];
  var types = [];
  $( ".contact-type-picker.selected" ).each(function( index ) {
    types.push($(this).attr('id'));
  });

  if (types.length == 2) {
    contact_type = 'Both';
  }
  else {
    contact_type = $( ".contact-type-picker.selected" ).html();
  }

  $( ".group-picker.selected" ).each(function( index ) {
    groups.push($(this).attr('id'));
  });
  var name = $('#saveContactName').val();
  var msisdn = $('#saveContactMsisdn').val();
  $.post('/contact/save',
    {
      type:'save',
      name:name,
      msisdn:msisdn,
      groups:groups,
      contact_type:contact_type
    },
    function(data){
      $('#saveContactBtn').button('complete');
      $('#saveContactModal').modal('hide');
      $('.content').html(data);
    });
}

function add_contact() {
  $('#addContactBtn').button('loading');

  var groups = [];
  var types = [];
  $( ".contact-type-picker.add-contact-picker.selected").each(function( index ) {
    types.push($(this).attr('id'));
  });

  if (types.length == 2) {
    contact_type = 'Both';
  }
  else {
    contact_type = $( ".contact-type-picker.add-contact-picker.selected" ).html();
  }

  $( ".group-picker.add-contact-picker.selected" ).each(function( index ) {
    groups.push($(this).attr('id'));
  });
  var name = $('#addContactName').val();
  var msisdn = $('#addContactMsisdn').val();
  $.post('/contact/save',
    {
      type:'add',
      name:name,
      msisdn:msisdn,
      groups:groups,
      contact_type:contact_type
    },
    function(data){
      $('#addContactModal').modal('hide');
      $('.content').html(data);
      $('#addContactBtn').button('complete');
      $('#addContactBtn').attr('disabled', true);
    });
}

function edit_contact(type) {
  $('#editContactBtn').button('loading');

  var groups = [];
  var types = [];
  $( ".contact-type-picker.edit-contact-picker.selected").each(function( index ) {
    types.push($(this).attr('id'));
  });

  if (types.length == 2) {
    contact_type = 'Both';
  }
  else {
    contact_type = $( ".contact-type-picker.edit-contact-picker.selected" ).html();
  }
  $( ".group-picker.edit-contact-picker.selected" ).each(function( index ) {
    groups.push($(this).attr('id'));
  });
  var name = $('#editContactName').val();
  var msisdn = $('#editContactMsisdn').val();
  $.post('/contact/edit',
    {
      type:type,
      name:name,
      msisdn:msisdn,
      groups:groups,
      contact_type:contact_type
    },
    function(data){
      $('#editContactModal').modal('hide');
      $('.content').html(data);
      $('#editContactBtn').button('complete');
      $('#editContactBtn').attr('disabled', true);
    });
}

function supply_contact_info() {
  var msisdn = $('#hiddenMsisdn').val();
  $.get('/contact',
    {
      type:'from_convo',
      msisdn:msisdn
    },
    function(data){
      $('#editContactModal .modal-content').html(data);
      $('#editContactModal .form-control').change();
    });
}

function supply_info_from_contacts(msisdn) {
  $.get('/contact',
    {
      type:'from_contacts',
      msisdn:msisdn
    },
    function(data){
      $('#editContactModal .modal-content').html(data);
      $('#editContactModal .form-control').change();
    });
}

function send_reply() {
  $('#sendReplyBtn').button('loading');
  var content = $('#conversationReply').val();
  $.post('/conversation/reply',
    {
      content:content
    },
    function(data){
      $('#sendReplyBtn').button('complete');
      if (data['status'] == 'success') {
        $('.conversation-container').append(data['template']);
        $('#conversationReply').val('');
        $('#replyCharacterCounter').val('Remaining: 420');
        $('#replySuccess').fadeIn();
        $("html, body").animate({ scrollTop: $(document).height()-$(window).height() });
        setTimeout(function() {
          $('#sendReplyBtn').attr('disabled', true);
        }, 0);
        setTimeout(function() {
          $('#replySuccess').fadeOut();
        }, 4000);
      }
      else {
        $('#replyError').fadeIn();
        setTimeout(function() {
          $('#replyError').fadeOut();
        }, 4000);
      }
    });
}

function initialize_recipients() {
  group_recipients = [];
  individual_recipients = [];
  group_recipients_name = [];
  individual_recipients_name = [];
  total_recipients = 0;
  $('.recipient-group').removeClass('selected');
  $('.recipient-contact').removeClass('selected');
  $('#recipientContainer').html('<span class="empty-recipient-label">Recipients</span>');
  $('.add-recipient-right-body').html('<div class="no-recipient"><span>Empty</span></div>');
}

function add_recipient(id,name,size) {
  $('#'+id+'.recipient-group').toggleClass('selected');
  if ($('#'+id+'.recipient-group').hasClass('selected')) {
    group_recipients.push(id);
    group_recipients_name.push(name);
    total_recipients += parseInt(size);
    $('.add-recipient-right-body').append("<div id='"+id+"' class='active-recipient group'><span class='active-recipient-name'>"+name+" ("+size+")</span><div class='remove-recipient-container'><span class='remove-recipient' onclick='remove_group_recipient("+id+","+size+","+name+")'><i class='material-icons remove-recipient-icon'>&#xE5CD;</i></span></div></div>");
  }
  else {
    remove_group_recipient(id,size,name);
  }
  $('#recipientCount').html('('+total_recipients+')');
  if ((group_recipients.length == 0) && (individual_recipients.length == 0)) {
    $('.no-recipient').show();
  }
  else {
    $('.no-recipient').hide();
  }
}

function add_individual_recipient(id,name) {
  $('#'+id+'.recipient-contact').toggleClass('selected');
  if ($('#'+id+'.recipient-contact').hasClass('selected')) {
    individual_recipients.push(id);
    individual_recipients_name.push(name);
    total_recipients += 1;
    $('.add-recipient-right-body').append("<div id='"+id+"' class='active-recipient individual'><span class='active-recipient-name'>"+name+"</span><div class='remove-recipient-container'><span class='remove-recipient' onclick='remove_individual_recipient("+id+","+name+")'><i class='material-icons remove-recipient-icon'>&#xE5CD;</i></span></div></div>")
  }
  else {
    return remove_individual_recipient(id,name);
  }
  $('#recipientCount').html('('+total_recipients+')');
  if ((group_recipients.length == 0) && (individual_recipients.length == 0)) {
    $('.no-recipient').show();
  }
  else {
    $('.no-recipient').hide();
  }
}

function remove_individual_recipient(id,name) {
  var id_index = individual_recipients.indexOf(id);
  var name_index = individual_recipients.indexOf(name);
  individual_recipients.splice(id_index, 1);
  individual_recipients_name.splice(name_index, 1);
  total_recipients -= 1;
  $('#'+id+'.active-recipient.individual').remove()
  $('#'+id+'.recipient-contact').removeClass('selected');
  $('#recipientCount').html('('+total_recipients+')');
  if ((group_recipients.length == 0) && (individual_recipients.length == 0)) {
    $('.no-recipient').show();
  }
  else {
    $('.no-recipient').hide();
  }
  return
}

function remove_group_recipient(id,size,name) {
  var id_index = group_recipients.indexOf(id);
  var name_index = group_recipients.indexOf(name);
  group_recipients.splice(id_index, 1);
  group_recipients_name.splice(name_index, 1);
  total_recipients -= parseInt(size);
  $('#'+id+'.active-recipient.group').remove()
  $('#'+id+'.recipient-group').removeClass('selected');
  $('#recipientCount').html('('+total_recipients+')');
  if ((group_recipients.length == 0) && (individual_recipients.length == 0)) {
    $('.no-recipient').show();
  }
  else {
    $('.no-recipient').hide();
  }
  return
}

function save_recipients() {
  $.post('/recipients/add',
    {
      individual_recipients_name:individual_recipients_name,
      group_recipients_name:group_recipients_name
    },
    function(data){
      $('#addRecipientModal').modal('hide');
      $('#recipientContainer').html(data);
    });
}

function send_text_blast() {
  $('#sendMessageBtn').button('loading');
  var content = $('#messageBody').val();
  $.post('/blast/send',
    {
      content:content,
      individual_recipients:individual_recipients,
      group_recipients:group_recipients,
      individual_recipients_name:individual_recipients_name,
      group_recipients_name:group_recipients_name,
      total_recipients:total_recipients
    },
    function(data){
      $('#sendMessageBtn').button('complete');
      $('#messageContainer').hide();
      $('#messageBody').val('');
      initialize_recipients();
      $('#blastOverlay .blast-overlay-body').html(data['template']);
      $('#blastOverlay').removeClass('hidden');

      if (data['pending'] != 0) {
        refresh_blast_progress(data['batch_id']);
      }
    });
}

function refresh_blast_progress(batch_id) {
  $.post('/blast/progress',
    {
      batch_id:batch_id
    },
    function(data){
      $('#blastOverlay .blast-overlay-body').html(data['template']);
      if (data['pending'] != 0) {
        console.log('working');
        refresh_blast_progress(batch_id);
      }
      else {
        display_blast_report(batch_id);
      }
    });
}

function refresh_reminder_progress(batch_id) {
  $.post('/reminder/progress',
    {
      batch_id:batch_id
    },
    function(data){
      $('#blastOverlay .blast-overlay-body').html(data['template']);
      if (data['pending'] != 0) {
        console.log('working');
        refresh_reminder_progress(batch_id);
      }
      else {
        display_reminder_report(batch_id);
      }
    });
}

function hide_blast_progress() {
  $('#blastOverlay').addClass('hidden');
}

function display_blast_report(batch_id) {
  $.post('/blast/summary',
    {
      batch_id:batch_id
    },
    function(data){
      $('#blastOverlay .blast-overlay-body').append(data);
    });
}

function display_reminder_report(batch_id) {
  $.post('/reminder/summary',
    {
      batch_id:batch_id
    },
    function(data){
      $('#blastOverlay .blast-overlay-body').append(data);
    });
}

function send_reminder() {
  $('#sendReminderBtn').button('loading');
  setTimeout(function(){
    var form_data = new FormData($('#uploadFileForm')[0]);
    $.ajax({
        type: 'POST',
        url: '/reminder/upload',
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        async: false,
        success: function(data) {
          if (data['status'] == 'success') {
            $('#fileErrorMessage').addClass('hidden');
            $('#addReminderModal').modal('hide');
            $('#blastOverlay .blast-overlay-body').html(data['template']);
            $('#blastOverlay').removeClass('hidden');
            if (data['pending'] != 0) {
              refresh_reminder_progress(data['batch_id']);
            }
            $('#sendReminderBtn').button('complete');
          }
          else {
            $('#fileErrorMessage').html(data['message']);
            $('#fileErrorMessage').removeClass('hidden');
            $('#sendReminderBtn').button('complete');
          }
        },
    });
  }, 800);
}

function save_group() {
  var name = $('#addGroupName').val();
  $.post('/groups/save',
    {
      name:name
    },
    function(data){
      if (data['status'] == 'success') {
        $('#createGroupModal').hide();
        $('#addGroupName').val('');
        $('.content').html(data['template']);
      }
    });
}

function open_blast(batch_id) {
  $.get('/blast',
    {
      batch_id:batch_id
    },
    function(data){
      $('.content').html(data);
    });
}

function open_reminder(reminder_id) {
  $.get('/reminder',
    {
      reminder_id:reminder_id
    },
    function(data){
      $('#viewReminderModal .modal-body').html(data);
    });
}

function check_upload_progress() {
  $.get('/progress/existing',
    function(data){
      if (data['in_progress'] == 'blast') {
        $('#blastOverlay .blast-overlay-body').html(data['template']);
        $('#blastOverlay').removeClass('hidden');
        if (data['pending'] != 0) {
          refresh_blast_progress(data['batch_id']);
        }
      }
      else if (data['in_progress'] == 'reminder') {
        $('#blastOverlay .blast-overlay-body').html(data['template']);
        $('#blastOverlay').removeClass('hidden');
        if (data['pending'] != 0) {
          refresh_reminder_progress(data['batch_id']);
        }
      }
    });
}