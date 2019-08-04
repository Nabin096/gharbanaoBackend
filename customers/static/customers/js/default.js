$(document).ready(function() {
	$('[data-toggle="offcanvas"]').click(function(){
		$('#side-menu').toggleClass('hidden-xs');
		
	})
	
})





$(document).ready(function() {
$(".btn-pref .btn").click(function () {
    $(".btn-pref .btn").removeClass("btn-primary").addClass("btn-default");
    // $(".tab").addClass("active"); // instead of this do the below 
    $(this).removeClass("btn-default").addClass("btn-primary");   
});
});





$('#myCarousel').carousel({
interval: 4000
});





$('#myModal').on('shown.bs.modal', function () {
  $('#myInput').focus()
})


$('#myModaler').on('shown.bs.modal', function () {
  $('#myInput').focus()
})
















