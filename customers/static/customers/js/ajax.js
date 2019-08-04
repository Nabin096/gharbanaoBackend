$(document).ready(function(){

  $('#name').keyup(function(e){
      e.preventDefault();
     $.ajax({
           type: "POST",
           url:"designs",
           data: {
              'search_text': $('#name').val(),
              'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val()
           },
           success:searchSuccess,
           dataType:'html',

     });

  }

);



});


function searchSuccess(data,textStatus,jqXHR){

    $('#test').html(data);
    $('#test li').click(function(e){
         e.preventDefault();
         $('#name').val(this.innerHTML);
    });

}







