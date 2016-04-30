//IIFE for navTabs
(function() {
    

}) ();

$(".singleWell").on("click", function() {
    $("#singleModal").modal("show");
});


$(".submitSingle").on("click", function() {

    //Front end error checking with toast messaging.
    



    $(this).prop("disabled", true).text("Sent").removeClass("btn-primary").addClass("btn-success");
    $.ajax({
        url: '/sRegistration',
        data: $('#singleForm').serialize(),
        type: 'POST',
        success: function(response) {
            console.log(response)
        }
    })
}); 

$("#singleModal").on("hidden.bs.modal", function() {
    $(this).prop("disabled", false).text("Send").addClass("btn-primary").removeClass("btn-success");
});

$("#formLogin").on("submit", function(event) {
    event.preventDefault();
    $.ajax({
        url: '/userLogin',
        data: $('#formLogin').serialize(),
        type: 'POST',
        success: function(response) {
            console.log(response)
        }
    })

})


