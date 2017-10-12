function upload_file(){
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
        $('.main').html(data);
        $('#uploadBtn').button('complete');
      },
  });
}
    