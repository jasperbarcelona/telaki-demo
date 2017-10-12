$(document).ready(function(){

$('#uploadBtn').on('click', function () {
    $('#file').click();
});

$('#file').on('change', function () {
    $('#uploadFileForm').submit();
});

$('#uploadFileForm').on('submit', function (e) {
    e.preventDefault();
    $('#uploadBtn').button('loading');
    upload_file();
});

});