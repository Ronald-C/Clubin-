$(".singleWell").on("click", function() {
    $("#singleModal").modal("show");
});


$(".submitSingle").on("click", function() {
    $.ajax({
        url: '/sRegistration',
        data: $('#singleForm').serialize(),
        type: 'POST',

        success: function(response) {
            console.log(response)
        }
    })