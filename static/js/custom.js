//IIFE for navTabs
(function() {
    var pathTab = {};
    pathTab["signup"] = "signUpTab";
    pathTab["login"] = "loginTab";

    for( var key in pathTab) {
            if( window.location.href.indexOf( key ) > -1 ){
                $("#" + pathTab[key] ).addClass("active");
                return;
        }
    }
        $("#homeTab").addClass("active");

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
    // event.preventDefault();
    // $.ajax({
    //     url: '/userLogin',
    //     data: $('#formLogin').serialize(),
    //     type: 'POST',
    //     success: function(response) {
    //         console.log(response)
    //     }
    // })

})


