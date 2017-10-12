function upload_file() {
  var form_data = new FormData($('#uploadFileForm')[0]);
  $.ajax({
      type: 'POST',
      url: '/upload',
      data: form_data,
      contentType: false,
      cache: false,
      processData: false,
      async: false,
      success: function(data) {
        $('.main').html(data['template']);
        update(data['batch_id'])
      },
  });
}

function update(batch_id) {
   setTimeout(function(){
      $.post('/message/status/get',{
        batch_id:batch_id
      },
      function(data){
        $('#poc-done').html(data['done']);
        if (data['pending'] != 0) {
          update(batch_id);
        }
        else {
          $('#sendAnotherBtn').show();
        }
      });
  }, 0);
};

function refresh_main(){
  $.post('/refresh',
  function(data){
    $('.main').html(data);
  });
}