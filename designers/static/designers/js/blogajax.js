$(document).ready(function(){

  $("#LikeForm").on('submit',function(e){


      var postData=$(this).serializeArray();
      var formURL=$(this).attr("action");
      $.ajax({
          url : formURL,
          type: "POST",
          data:{
              'values': $('#likebutton').val(),
              'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val()
           },
          success:function(data,textStatus,jqXHR){
               alert("running");
          },
          error:function(jqXHR,textStatus,errorThrown)
          {

          },
          dataType:'html',
      });


       e.preventDefault();
       return false;
  });
  $("#LikeForm").submit();
});

