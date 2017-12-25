$(document).ready(function(){

var isPreviousEventComplete = true;

/*$('tbody').scroll(function () {
    if($(this).scrollTop() + $(this).height() > (this.scrollHeight * .7))  {
        var that = this;
        if (isPreviousEventComplete) {
            if(searchStatus == 'off'){
                load_next(String(that.getAttribute('id')));
            }
            else{
                eval(String(that.getAttribute('id'))+'_next_search()');
            }
        }
    }
});*/
$('tbody').scroll(function () {
    var $this = jQuery(this);
    if ($this.data('activated')) return false;  // Pending, return

    if($(this).scrollTop() + $(this).height() > (this.scrollHeight * .95)) {
        if(isPreviousEventComplete){
            if(searchStatus == 'off'){
                load_next(String(this.getAttribute('id')));
                console.log('loading next');
                $this.data('activated', true);
            }
            else{
                eval(String(this.getAttribute('id'))+'_next_search()');
                $this.data('activated', true);
            }
        }
    }
});

});