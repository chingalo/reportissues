$(document).ready(function(){
   //animation for all neccessary info for system
   //delay() slideUp() fadeOut() show() hide()
   //event 1
   $(".event1").hide().show(2000).delay(2000).hide(2000).delay(12000).show(2000).delay(2000).hide(2000);
   
   
   //event 2
   $(".event2").hide().delay(4000).show(2000).delay(2000).slideUp(2000).delay(12000).show(2000).delay(2000).hide(2000);
   
   
   //event 3.
   $(".event3").hide().delay(8000).show(2000).delay(2000).hide(2000).delay(12000).show(2000).delay(2000).slideUp(2000);
   
   
   //event 4
   $(".event4").hide().delay(12000).fadeIn(2000).delay(2000).slideUp(2000).delay(12000).show(2000).delay(2000).hide(2000);
   
   
});
