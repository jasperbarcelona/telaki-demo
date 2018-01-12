/* NAVIGATION */

function show_conversations(slice_from) {
  $('.panel-nav-item').removeClass('active');
  $('#navConversations').addClass('active');
  $.get('/conversations',
  {
    slice_from:slice_from
  },
    function(data){
      initialize_selected_entries();
      $('.content').html(data);
      $('#searchLoader').addClass('hidden');
      $('#clearConversationsSearch').addClass('hidden');
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
      initialize_selected_entries();
      $('.content').html(data);
      $('#searchLoader').addClass('hidden');
      $('#clearConversationsSearch').addClass('hidden');
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
      initialize_selected_entries();
      $('.content').html(data);
      $('#searchLoader').addClass('hidden');
      $('#clearConversationsSearch').addClass('hidden');
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
      initialize_selected_entries();
      $('.content').html(data);
      $('#searchLoader').addClass('hidden');
      $('#clearConversationsSearch').addClass('hidden');
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
      initialize_selected_entries();
      $('.content').html(data);
      $('#searchLoader').addClass('hidden');
      $('#clearConversationsSearch').addClass('hidden');
    });
}

/* END OF NAVIGATION */

/* START OF PAGINATION */

function conversation_next_page() {
  $.post('/conversations/next',
    function(data){
      initialize_selected_entries();
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
      initialize_selected_entries();
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
      initialize_selected_entries();
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
      initialize_selected_entries();
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
      initialize_selected_entries();
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
      initialize_selected_entries();
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
      initialize_selected_entries();
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
      initialize_selected_entries();
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
      initialize_selected_entries();
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
      initialize_selected_entries();
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
      initialize_selected_entries();
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
      initialize_selected_entries();
      $('#editContactModal .modal-content').html(data);
      $('#editContactModal .form-control').change();
    });
}

function open_group(group_id) {
  $.get('/group',
    {
      group_id:group_id
    },
    function(data){
      initialize_selected_entries();
      $('#groupMembersModal .modal-body').html(data);
      $('#groupMembersModal .form-control').change();
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

function initialize_selected_entries() {
  selected_conversations = [];
  selected_blasts = [];
  selected_reminders = [];
  selected_contacts = [];
  selected_groups = [];

  $('#deleteConversationsBtn').addClass('hidden');
  $('#deleteBlastsBtn').addClass('hidden');
  $('#deleteRemindersBtn').addClass('hidden');
  $('#deleteContactsBtn').addClass('hidden');
  $('#deleteGroupsBtn').addClass('hidden');
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
      $('body').css('overflow-y','hidden');
      if (data['pending'] != 0) {
        refresh_blast_progress(data['batch_id']);
      }
      else {
        display_blast_report(data['batch_id']);
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
        refresh_reminder_progress(batch_id);
      }
      else {
        display_reminder_report(batch_id);
      }
    });
}

function refresh_contacts_progress(batch_id) {
  $.post('/contacts/progress',
    {
      batch_id:batch_id
    },
    function(data){
      $('#blastOverlay .blast-overlay-body').html(data['template']);
      if (data['pending'] != 0) {
        refresh_contacts_progress(batch_id);
      }
      else {
        display_contacts_report(batch_id);
      }
    });
}

function hide_blast_progress() {
  $('#blastOverlay').addClass('hidden');
  $('body').css('overflow-y','scroll');
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

function display_contacts_report(batch_id) {
  $.post('/contacts/summary',
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
            $('body').css('overflow-y','hidden');
            if (data['pending'] != 0) {
              refresh_reminder_progress(data['batch_id']);
            }
            else {
              display_reminder_report(data['batch_id']);
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

function upload_contacts() {
  $('#uploadContactsBtn').button('loading');
  setTimeout(function(){
    var form_data = new FormData($('#uploadContactsForm')[0]);
    $.ajax({
        type: 'POST',
        url: '/contacts/upload',
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        async: false,
        success: function(data) {
          if (data['status'] == 'success') {
            $('#contactsFileErrorMessage').addClass('hidden');
            $('#uploadContactsModal').modal('hide');
            $('#blastOverlay .blast-overlay-body').html(data['template']);
            $('#blastOverlay').removeClass('hidden');
            $('body').css('overflow-y','hidden');
            if (data['pending'] != 0) {
              refresh_contacts_progress(data['batch_id']);
            }
            else {
              display_contacts_report(data['batch_id']);
            }
            $('#uploadContactsBtn').button('complete');
          }
          else {
            $('#contactsFileErrorMessage').html(data['message']);
            $('#contactsFileErrorMessage').removeClass('hidden');
            $('#uploadContactsBtn').button('complete');
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
      initialize_selected_entries();
      $('.content').html(data);
    });
}

function open_reminder(reminder_id) {
  $.get('/reminder',
    {
      reminder_id:reminder_id
    },
    function(data){
      initialize_selected_entries();
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

function search_conversations(active_text) {
  $('#conversationsTbody').html('');
  $('#searchLoader').removeClass('hidden');
  $('#clearConversationsSearch').removeClass('hidden');
  var name = $('#searchConversationName').val();
  var content = $('#searchConversationContent').val();
  var date = $('#searchConversationDate').val();
  if ((name == '') && (content == '') && (date == '')) {
    $.get('/conversations',
    {
      slice_from:'reset'
    },
    function(data){
      initialize_selected_entries();
      $('.content').html(data);
      $('#searchLoader').addClass('hidden');
      $('#clearConversationsSearch').addClass('hidden');
      $('#'+active_text).focus();
    });
  }
  else {
    $.get('/conversations/search',
    {
      name:name,
      content:content,
      date:date
    },
    function(data){
      $('#conversationsTbody').html(data['template']);
      $('#searchLoader').addClass('hidden');
      if (data['count'] != 0) {
        var start_from = 1;
      }
      else {
        var start_from = 0;
      }
      $('#paginationShowingConversation').html(start_from+' to '+data['count']);
      $('#paginationTotalConversation').html(data['count']);
      $('.pagination-btn').attr('disabled',true);
    });
  }
}

function search_blasts(active_text) {
  $('#blastsTbody').html('');
  $('#searchLoader').removeClass('hidden');
  $('#clearBlastsSearch').removeClass('hidden');
  var sender = $('#searchBlastsSender').val();
  var content = $('#searchBlastsContent').val();
  var date = $('#searchBlastsDate').val();
  if ((sender == '') && (content == '') && (date == '')) {
    $.get('/blasts',
    {
      slice_from:'reset'
    },
    function(data){
      initialize_selected_entries();
      $('.content').html(data);
      $('#searchLoader').addClass('hidden');
      $('#clearBlastsSearch').addClass('hidden');
      $('#'+active_text).focus();
    });
  }
  else {
    $.get('/blasts/search',
    {
      sender:sender,
      content:content,
      date:date
    },
    function(data){
      $('#blastsTbody').html(data['template']);
      $('#searchLoader').addClass('hidden');
      if (data['count'] != 0) {
        var start_from = 1;
      }
      else {
        var start_from = 0;
      }
      $('#paginationShowingBlasts').html(start_from+' to '+data['count']);
      $('#paginationTotalBlasts').html(data['count']);
      $('.pagination-btn').attr('disabled',true);
    });
  }
}

function search_reminders(active_text) {
  $('#remindersTbody').html('');
  $('#searchLoader').removeClass('hidden');
  $('#clearRemindersSearch').removeClass('hidden');
  var sender = $('#searchRemindersSender').val();
  var filename = $('#searchRemindersFile').val();
  var date = $('#searchRemindersDate').val();
  if ((sender == '') && (filename == '') && (date == '')) {
    $.get('/reminders',
    {
      slice_from:'reset'
    },
    function(data){
      initialize_selected_entries();
      $('.content').html(data);
      $('#searchLoader').addClass('hidden');
      $('#clearRemindersSearch').addClass('hidden');
      $('#'+active_text).focus();
    });
  }
  else {
    $.get('/reminders/search',
    {
      sender:sender,
      filename:filename,
      date:date
    },
    function(data){
      $('#remindersTbody').html(data['template']);
      $('#searchLoader').addClass('hidden');
      if (data['count'] != 0) {
        var start_from = 1;
      }
      else {
        var start_from = 0;
      }
      $('#paginationShowingReminders').html(start_from+' to '+data['count']);
      $('#paginationTotalReminders').html(data['count']);
      $('.pagination-btn').attr('disabled',true);
    });
  }
}

function search_contacts(active_text) {
  $('#contactsTbody').html('');
  $('#searchLoader').removeClass('hidden');
  $('#clearContactsSearch').removeClass('hidden');
  var name = $('#searchContactsName').val();
  var contact_type = $('#searchContactsType').val();
  var msisdn = $('#searchContactsMsisdn').val();
  if ((name == '') && (contact_type == '') && (msisdn == '')) {
    $.get('/contacts',
    {
      slice_from:'reset'
    },
    function(data){
      initialize_selected_entries();
      $('.content').html(data);
      $('#searchLoader').addClass('hidden');
      $('#clearContactsSearch').addClass('hidden');
      $('#'+active_text).focus();
    });
  }
  else {
    $.get('/contacts/search',
    {
      name:name,
      contact_type:contact_type,
      msisdn:msisdn
    },
    function(data){
      $('#contactsTbody').html(data['template']);
      $('#searchLoader').addClass('hidden');
      if (data['count'] != 0) {
        var start_from = 1;
      }
      else {
        var start_from = 0;
      }
      $('#paginationShowingContacts').html(start_from+' to '+data['count']);
      $('#paginationTotalContacts').html(data['count']);
      $('.pagination-btn').attr('disabled',true);
    });
  }
}

function search_groups(active_text) {
  $('#groupsTbody').html('');
  $('#searchLoader').removeClass('hidden');
  $('#clearGroupsSearch').removeClass('hidden');
  var name = $('#searchGroupsName').val();
  if (name == '') {
    $.get('/groups',
    {
      slice_from:'reset'
    },
    function(data){
      initialize_selected_entries();
      $('.content').html(data);
      $('#searchLoader').addClass('hidden');
      $('#clearGroupsSearch').addClass('hidden');
      $('#'+active_text).focus();
    });
  }
  else {
    $.get('/groups/search',
    {
      name:name
    },
    function(data){
      $('#groupsTbody').html(data['template']);
      $('#searchLoader').addClass('hidden');
      if (data['count'] != 0) {
        var start_from = 1;
      }
      else {
        var start_from = 0;
      }
      $('#paginationShowingGroups').html(start_from+' to '+data['count']);
      $('#paginationTotalGroups').html(data['count']);
      $('.pagination-btn').attr('disabled',true);
    });
  }
}

function select_conversation(entry_id) {
  selected_conversations.push(entry_id);
}

function deselect_conversation(entry_id) {
  var entry_index = selected_conversations.indexOf(entry_id);
  selected_conversations.splice(entry_index, 1);
}

function select_blast(entry_id) {
  selected_blasts.push(entry_id);
  alert(selected_blasts);
}

function deselect_blast(entry_id) {
  var entry_index = selected_blasts.indexOf(entry_id);
  selected_blasts.splice(entry_index, 1);
  alert(selected_blasts);
}

function select_reminder(entry_id) {
  selected_reminders.push(entry_id);
  alert(selected_reminders);
}

function deselect_reminder(entry_id) {
  var entry_index = selected_reminders.indexOf(entry_id);
  selected_reminders.splice(entry_index, 1);
  alert(selected_reminders);
}

function select_contact(entry_id) {
  selected_contacts.push(entry_id);
  alert(selected_contacts);
}

function deselect_contact(entry_id) {
  var entry_index = selected_contacts.indexOf(entry_id);
  selected_contacts.splice(entry_index, 1);
  alert(selected_contacts);
}

function select_group(entry_id) {
  selected_groups.push(entry_id);
  alert(selected_groups);
}

function deselect_group(entry_id) {
  var entry_index = selected_groups.indexOf(entry_id);
  selected_groups.splice(entry_index, 1);
  alert(selected_groups);
}