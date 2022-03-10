$(document).ready(function(){
  $('body').on('click', '#items_en_uso span', function(){
    alert($(this).attr('id'))
  })
});

var DELAY = 700,
    clicks = 0,
    timer = null;

$(document).ready(function() {

    $("a")
    .bind("click", function(e){

        clicks++;  //count clicks

        if(clicks === 1) {

            timer = setTimeout(function() {

                alert('Single Click'); //perform single-click action

                clicks = 0;  //after action performed, reset counter

            }, DELAY);

        } else {

            clearTimeout(timer);  //prevent single-click action

            alert('Double Click');  //perform double-click action

            clicks = 0;  //after action performed, reset counter
        }

    })
    .bind("dblclick", function(e){
        e.preventDefault();  //cancel system double-click event
    });

});
