$(document).ready(function(){
   //animation for all neccessary info for system
   //delay() slideUp() slideDown() fadeOut() fadeIn() show() hide()
   //event 1
   $(".event1").hide().show(2000).delay(1000).hide(2000);
   
   
   //event 2
   $(".event2").hide().delay(3000).show(2000).delay(1000).slideUp(2000);
   
   
   //event 3
   $(".event3").hide().delay(6000).show(2000).delay(1000).hide(2000);
   
   
   //event 4
   $(".event4").hide().delay(9000).fadeIn(2000).delay(1000);
   
   
});
