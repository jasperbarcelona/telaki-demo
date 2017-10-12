$(document).ready(function(){

onScrollInit( $('.below') );
onScrollInit( $('.advantages'), $('#page5') );

if (document.documentElement.clientWidth > 1000) {
        $('#page1-pic-container').css('height',($('#page1-pic-container').width()-200));
    }
    else{
        $('#page1-pic-container').css('height',($('#page1-pic-container').width()-170));
    }

$(window).resize(function() {
    if (document.documentElement.clientWidth > 1000) {
        $('#page1-pic-container').css('height',($('#page1-pic-container').width()-200));
    }
    else{
        $('#page1-pic-container').css('height',($('#page1-pic-container').width()-170));
    }
});

/*$(window).on('scroll', function(){
    if (document.documentElement.clientWidth > 1000){
        st = $('body').scrollTop();
        if(st >= 200){
            $("#floating-header").css("top","0");
        }
        else if (st<200){
            $("#floating-header").css("top","-80px");
        }
    }
});*/

function onScrollInit( items, trigger ) {
  items.each( function() {
    var osElement = $(this),
        osAnimationClass = osElement.attr('data-os-animation'),
        osAnimationDelay = osElement.attr('data-os-animation-delay');
 
    osElement.css({
        '-webkit-animation-delay':  osAnimationDelay,
        '-moz-animation-delay':     osAnimationDelay,
        'animation-delay':          osAnimationDelay
    });
 
    var osTrigger = ( trigger ) ? trigger : osElement;
 
    osTrigger.waypoint(function() {
        osElement.addClass('animated').addClass(osAnimationClass);
    },{
        triggerOnce: true,
        offset: '50%'
    });
  });
}

})