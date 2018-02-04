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

function show_users(slice_from) {
  alert('This feature will be available on paid version.');
}

function show_usage(slice_from) {
  alert('This feature will be available on paid version.');
}

function user_profile() {
  alert('This feature will be available on paid version.');
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

  $( ".group-picker-save.selected" ).each(function( index ) {
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
      $('#saveContactModal .form-control').val('');
      $('#saveContactModal .contact-type-picker').removeClass('selected');
      $('#saveContactModal .group-picker').removeClass('selected');
      $('#saveContactModal .form-control').change();
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

  $( ".group-picker-add.selected" ).each(function( index ) {
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
      $('#addContactModal .form-control').val('');
      $('#addContactModal .contact-type-picker').removeClass('selected');
      $('#addContactModal .group-picker').removeClass('selected');
      $('#addContactModal .form-control').change();
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
  $( ".group-picker-edit.selected" ).each(function( index ) {
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

function save_group_change() {
  var group_name = $('#editGroupName').val();
  $.post('/group/edit',
    {
      group_name:group_name
    },
    function(data){
      show_groups('continue')
      $('#groupMembersModal').modal('hide');
    });
}

function delete_group_member() {
  $.post('/group/members/delete',
  function(data){
    $('#groupMembersModal .modal-body').html(data);
    $('#groupMembersModal .form-control').change();
    $('#deleteMemberModal').modal('hide');
  });
}

function get_delete_member(member_id, group_id) {
  $.post('/group/members/delete/get',
  {
    member_id:member_id,
    group_id:group_id
  },
  function(data){
    $('#deleteMemberModal').modal('show');
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
  special = undefined;
  total_recipients = 0;
  $('.no-recipient').show();
  $('#recipientCount').html('('+total_recipients+')');
  $('.recipient-group').removeClass('selected');
  $('.recipient-contact').removeClass('selected');
  $('#recipientContainer').html('<span class="empty-recipient-label">Recipients</span>');
  $('.add-recipient-right-body').html('<div class="no-recipient"><span>Empty</span></div>');
}

function add_recipient(recipient_id) {
  $('#'+recipient_id+'.recipient-group').toggleClass('selected');
  if ($('#'+recipient_id+'.recipient-group').hasClass('selected')) {
    $.post('/recipients/group/add',
    {
      recipient_id:recipient_id
    },
    function(data){
      $('.add-recipient-right-body').append(data['template']);
      total_recipients += parseInt(data['size']);
      $('#recipientCount').html('('+total_recipients+')');
      if (total_recipients == 0) {
        $('.no-recipient').show();
      }
      else {
        $('.no-recipient').hide();
      }
    });
  }

  else {
    remove_group_recipient(recipient_id);
  }
}

function add_everyone_recipient(size) {
  $('#everyoneRecipient').toggleClass('selected');
  if ($('#everyoneRecipient').hasClass('selected')) {
    total_recipients = parseInt(size);
    $('.recipient-group:not(#everyoneRecipient)').addClass('disabled');
    $('.recipient-group:not(#everyoneRecipient)').removeClass('selected');
    $('.recipient-contact').addClass('disabled');
    $('.recipient-contact').removeClass('selected');
    $('.active-recipient.group').remove();
    $('.active-recipient.individual').remove();
    $('.add-recipient-right-body').append("<div id='everyoneRecipient' class='active-recipient group'><span class='active-recipient-name'>Everyone ("+size+")</span><div class='remove-recipient-container'><span class='remove-recipient' onclick='remove_everyone_recipient("+size+")'><i class='material-icons remove-recipient-icon'>&#xE5CD;</i></span></div></div>");
    $.post('/recipients/special/add',
    function(data){
      $('.add-recipient-right-body').append(data['template']);
      total_recipients = parseInt(data['size']);
      total_recipients += parseInt(size);
      $('#recipientCount').html('('+total_recipients+')');
      if (total_recipients == 0) {
        $('.no-recipient').show();
      }
      else {
        $('.no-recipient').hide();
      }
    });
  }
  else {
    remove_everyone_recipient(size);
  }
}

function add_customers_recipient(size) {
  $('#customersRecipient').toggleClass('selected');
  if ($('#customersRecipient').hasClass('selected')) {
    total_recipients = parseInt(size);
    $('.recipient-group:not(#customersRecipient)').addClass('disabled');
    $('.recipient-group:not(#customersRecipient)').removeClass('selected');
    $('.recipient-contact').addClass('disabled');
    $('.recipient-contact').removeClass('selected');
    $('.active-recipient:not(#customersRecipient)').remove();
    individual_recipients = [];
    group_recipients = [];
    individual_recipients_name = [];
    group_recipients_name = [];
    $('.add-recipient-right-body').append("<div id='customersRecipient' class='active-recipient group'><span class='active-recipient-name'>All Customers ("+size+")</span><div class='remove-recipient-container'><span class='remove-recipient' onclick='remove_customers_recipient("+size+")'><i class='material-icons remove-recipient-icon'>&#xE5CD;</i></span></div></div>");
  }
  else {
    remove_customers_recipient(size);
  }
  $('#recipientCount').html('('+total_recipients+')');
  if (total_recipients == 0) {
    $('.no-recipient').show();
  }
  else {
    $('.no-recipient').hide();
  }
}

function add_staff_recipient(size) {
  $('#staffRecipient').toggleClass('selected');
  if ($('#staffRecipient').hasClass('selected')) {
    total_recipients = parseInt(size);
    $('.recipient-group:not(#staffRecipient)').addClass('disabled');
    $('.recipient-group:not(#staffRecipient)').removeClass('selected');
    $('.recipient-contact').addClass('disabled');
    $('.recipient-contact').removeClass('selected');
    $('.active-recipient:not(#staffRecipient)').remove();
    individual_recipients = [];
    group_recipients = [];
    individual_recipients_name = [];
    group_recipients_name = [];
    $('.add-recipient-right-body').append("<div id='staffRecipient' class='active-recipient group'><span class='active-recipient-name'>All Staff ("+size+")</span><div class='remove-recipient-container'><span class='remove-recipient' onclick='remove_staff_recipient("+size+")'><i class='material-icons remove-recipient-icon'>&#xE5CD;</i></span></div></div>");
  }
  else {
    remove_staff_recipient(size);
  }
  $('#recipientCount').html('('+total_recipients+')');
  if (total_recipients == 0) {
    $('.no-recipient').show();
  }
  else {
    $('.no-recipient').hide();
  }
}

function remove_everyone_recipient(size) {
  total_recipients -= size;
  $('#everyoneRecipient.active-recipient').remove()
  $('#everyoneRecipient').removeClass('selected');
  $('.recipient-group:not(#everyoneRecipient)').removeClass('disabled');
  $('.recipient-contact').removeClass('disabled');
  $('#recipientCount').html('('+total_recipients+')');
  if (total_recipients == 0) {
    $('.no-recipient').show();
  }
  else {
    $('.no-recipient').hide();
  }
}

function remove_customers_recipient(size) {
  total_recipients -= size;
  $('#customersRecipient.active-recipient').remove()
  $('#customersRecipient').removeClass('selected');
  $('.recipient-group:not(#customersRecipient)').removeClass('disabled');
  $('.recipient-contact').removeClass('disabled');
  $('#recipientCount').html('('+total_recipients+')');
  if (total_recipients == 0) {
    $('.no-recipient').show();
  }
  else {
    $('.no-recipient').hide();
  }
}

function remove_staff_recipient(size) {
  total_recipients -= size;
  $('#staffRecipient.active-recipient').remove()
  $('#staffRecipient').removeClass('selected');
  $('.recipient-group:not(#staffRecipient)').removeClass('disabled');
  $('.recipient-contact').removeClass('disabled');
  $('#recipientCount').html('('+total_recipients+')');
  if (total_recipients == 0) {
    $('.no-recipient').show();
  }
  else {
    $('.no-recipient').hide();
  }
}

function add_individual_recipient(recipient_id) {
  $('#'+recipient_id+'.recipient-contact').toggleClass('selected');
  if ($('#'+recipient_id+'.recipient-contact').hasClass('selected')) {
   $.post('/recipients/individual/add',
    {
      recipient_id:recipient_id
    },
    function(data){
      $('.add-recipient-right-body').append(data['template']);
      total_recipients += 1;
      $('#recipientCount').html('('+total_recipients+')');
      if (total_recipients == 0) {
        $('.no-recipient').show();
      }
      else {
        $('.no-recipient').hide();
      }
    });
  }
  else {
    return remove_individual_recipient(recipient_id);
  }
  
}

function remove_individual_recipient(recipient_id) {
  $('#'+recipient_id+'.recipient-contact').removeClass('selected');
  $.post('/recipients/individual/remove',
  {
    recipient_id:recipient_id
  },
  function(data){
    $('#'+recipient_id+'.active-recipient.individual').remove()
    total_recipients -= 1;
    $('#recipientCount').html('('+total_recipients+')');
    if (total_recipients == 0) {
      $('.no-recipient').show();
    }
    else {
      $('.no-recipient').hide();
    }
  });
  return
}

function remove_group_recipient(recipient_id) {
  $('#'+recipient_id+'.recipient-group').removeClass('selected');
  $.post('/recipients/group/remove',
  {
    recipient_id:recipient_id
  },
  function(data){
    $('#'+recipient_id+'.active-recipient.group').remove()
    total_recipients -= parseInt(data['size']);
    $('#recipientCount').html('('+total_recipients+')');
    if (total_recipients == 0) {
      $('.no-recipient').show();
    }
    else {
      $('.no-recipient').hide();
    }
  });
  return
}

function save_recipients() {
  if ($('#everyoneRecipient').hasClass('selected')) {
    special = 'Everyone';
  }
  else if ($('#customersRecipient').hasClass('selected')) {
    special = 'All Customers';
  }
  else if ($('#staffRecipient').hasClass('selected')) {
    special = 'All Staff';
  }
  else {
    special = undefined;
  }
  $.post('/recipients/add',
    {
      special:special
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
      total_recipients:total_recipients,
      special:special
    },
    function(data){
      $('#sendMessageBtn').button('complete');
      $('#messageContainer').hide();
      $('#messageBody').val('');
      initialize_recipients();
      $('.active-recipient').remove()
      $('.recipient-group').removeClass('selected');
      $('.recipient-contact').removeClass('selected');
      $('.recipient-group').removeClass('disabled');
      $('.recipient-contact').removeClass('disabled');
      $('#recipientCount').html('('+total_recipients+')');

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

function search_contact_groups() {
  $('#recipientGroupLoading').removeClass('hidden');
  var group_name = $('#searchContactGroups').val();
  $.post('/contacts/groups/search',
    {
      group_name:group_name,
      group_recipients:group_recipients
    },
    function(data){
      $('#recipientGroupContainer').html(data);
      $('#recipientGroupLoading').addClass('hidden');
    });
}

function search_contact_recipients() {
  $('#recipientContactLoading').removeClass('hidden');
  var name = $('#searchRecipientName').val();
  $.post('/contacts/indiv/search',
    {
      name:name,
      individual_recipients:individual_recipients
    },
    function(data){
      $('#recipientContactContainer').html(data);
      $('#recipientContactLoading').addClass('hidden');
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
        $('#addGroupName').change();
        $('#addGroupError').addClass('hidden');
        $('.content').html(data['template']);
      }
      else {
        $('#addGroupError').html(data['message']);
        $('#addGroupError').removeClass('hidden');
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
      else if (data['in_progress'] == 'contact') {
        $('#blastOverlay .blast-overlay-body').html(data['template']);
        $('#blastOverlay').removeClass('hidden');
        if (data['pending'] != 0) {
          refresh_contacts_progress(data['batch_id']);
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
      $('#clearContactsSearch').addClass('hidden');
      $('.content').html(data);
      $('#searchLoader').addClass('hidden');
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
  if (selected_conversations.length != 0) {
    $('#deleteConversationsBtn').removeClass('hidden');
  }
  else {
    $('#deleteConversationsBtn').addClass('hidden');
  }
}

function deselect_conversation(entry_id) {
  var entry_index = selected_conversations.indexOf(entry_id);
  selected_conversations.splice(entry_index, 1);
  if (selected_conversations.length != 0) {
    $('#deleteConversationsBtn').removeClass('hidden');
  }
  else {
    $('#deleteConversationsBtn').addClass('hidden');
  }
}

function select_blast(entry_id) {
  selected_blasts.push(entry_id);
  if (selected_blasts.length != 0) {
    $('#deleteBlastsBtn').removeClass('hidden');
  }
  else {
    $('#deleteBlastsBtn').addClass('hidden');
  }
}

function deselect_blast(entry_id) {
  var entry_index = selected_blasts.indexOf(entry_id);
  selected_blasts.splice(entry_index, 1);
  if (selected_blasts.length != 0) {
    $('#deleteBlastsBtn').removeClass('hidden');
  }
  else {
    $('#deleteBlastsBtn').addClass('hidden');
  }
}

function select_reminder(entry_id) {
  selected_reminders.push(entry_id);
  if (selected_reminders.length != 0) {
    $('#deleteRemindersBtn').removeClass('hidden');
  }
  else {
    $('#deleteRemindersBtn').addClass('hidden');
  }
}

function deselect_reminder(entry_id) {
  var entry_index = selected_reminders.indexOf(entry_id);
  selected_reminders.splice(entry_index, 1);
  if (selected_reminders.length != 0) {
    $('#deleteRemindersBtn').removeClass('hidden');
  }
  else {
    $('#deleteRemindersBtn').addClass('hidden');
  }
}

function select_contact(entry_id) {
  selected_contacts.push(entry_id);
  if (selected_contacts.length != 0) {
    $('#deleteContactsBtn').removeClass('hidden');
  }
  else {
    $('#deleteContactsBtn').addClass('hidden');
  }
}

function deselect_contact(entry_id) {
  var entry_index = selected_contacts.indexOf(entry_id);
  selected_contacts.splice(entry_index, 1);
  if (selected_contacts.length != 0) {
    $('#deleteContactsBtn').removeClass('hidden');
  }
  else {
    $('#deleteContactsBtn').addClass('hidden');
  }
}

function select_group(entry_id) {
  selected_groups.push(entry_id);
  if (selected_groups.length != 0) {
    $('#deleteGroupsBtn').removeClass('hidden');
  }
  else {
    $('#deleteGroupsBtn').addClass('hidden');
  }
}

function deselect_group(entry_id) {
  var entry_index = selected_groups.indexOf(entry_id);
  selected_groups.splice(entry_index, 1);
  if (selected_groups.length != 0) {
    $('#deleteGroupsBtn').removeClass('hidden');
  }
  else {
    $('#deleteGroupsBtn').addClass('hidden');
  }
}

function delete_conversations() {
  $.post('/conversations/delete',
  {
    selected_conversations:selected_conversations
  },
  function(data){
    show_conversations('continue');
    $('#deleteConversationsModal').modal('hide');
  });
}

function delete_blasts() {
  $.post('/blasts/delete',
  {
    selected_blasts:selected_blasts
  },
  function(data){
    show_blasts('continue');
    $('#deleteBlastsModal').modal('hide');
  });
}

function delete_reminders() {
  $.post('/reminders/delete',
  {
    selected_reminders:selected_reminders
  },
  function(data){
    show_payment_reminders('continue');
    $('#deleteRemindersModal').modal('hide');
  });
}

function delete_contacts() {
  $.post('/contacts/delete',
  {
    selected_contacts:selected_contacts
  },
  function(data){
    show_contacts('continue');
    $('#deleteContactsModal').modal('hide');
  });
}

function delete_groups() {
  $.post('/groups/delete',
  {
    selected_groups:selected_groups
  },
  function(data){
    show_groups('continue');
    $('#deleteGroupsModal').modal('hide');
  });
}

function add_number_recipient() {
  recipient = $('#addNumberRecipient').val();
  $.post('/recipients/number/add',
  {
    recipient:recipient
  },
  function(data){
    total_recipients += 1;
    $('#recipientCount').html('('+total_recipients+')');
    $('.add-recipient-right-body').append(data);
    $('#addNumberRecipient').val('');
    $('#addNumberRecipientBtn').attr('disabled',true);
    $('.no-recipient').hide();
  });
}

function remove_number_recipient(msisdn) {
  $.post('/recipients/number/remove',
  {
    msisdn:msisdn
  },
  function(data){
    $('#'+msisdn+'.active-recipient.number').remove()
    total_recipients -= 1;
    $('#recipientCount').html('('+total_recipients+')');
    if (total_recipients == 0) {
      $('.no-recipient').show();
    }
    else {
      $('.no-recipient').hide();
    }
  });
  return
}

function close_message() {
  initialize_recipients();
  $.post('/recipients/clear',
  function(data){
    $('#recipientContainer').html('<span class="empty-recipient-label">Recipients</span>');
  });
}

function toggle_group_save(group_id) {
  $('#'+group_id+'.group-picker-save').toggleClass('selected');
}

function toggle_group_add(group_id) {
  $('#'+group_id+'.group-picker-add').toggleClass('selected');
}

function toggle_group_edit(group_id) {
  $('#'+group_id+'.group-picker-edit').toggleClass('selected');
}