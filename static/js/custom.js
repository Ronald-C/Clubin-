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

$(".orgWell").on("click", function() {
    $("#orgModal").modal("show");
});


$(".submitSingle").on("click", function() {

    //Front end error checking with toast messaging.

        //Check for empty fields
        var someEmpty = $('.mandatory').filter(function(){
            return $.trim(this.value).length === 0;
        }).length > 0;


        if( someEmpty ) {
            toastr.clear();
            toastr["warning"]("Please give values for required inputs.");
            return;
        }


        var digits = $("#SJSUIDSingle").val();

        //Exactly 9 characters for SJSUID
        if( digits.length != 9 ) {
            toastr["warning"]("Please enter exactly 9 digits for your SJSUID.");
            return;
        }


        //Numbers only fo SJSUID
        if( !$.isNumeric(digits) ) {
            toastr["warning"]("Numbers only for SJSUID");
            return;
            // your code here
        }

        //Passwords don't match
        var p1 = $("#PasswordSingle").val();
        var p2 = $("#PasswordSingleAgain").val();
        if( p1 != p2 ) {
            toastr["warning"]("Your passwords don't match.");
            return;
        }

        if(p1.length < 6) {
            toastr["warning"]("Your password is not long enough. Six character minimum.");
            return;
        }

        //Password doesn't have all StormPath requirements
        // var storm = new RegExp("^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{6,16}$/");
        // if(storm.test(p1)) {
        //     alert("Pass");

        // }

        var storm = /((?=.*d)(?=.*[a-z])(?=.*[A-Z]).{8,15})/gm;

    



    $(this).prop("disabled", true).text("Sent").removeClass("btn-primary").addClass("btn-success");
    $.ajax({
        url: '/sRegistration',
        data: $('#singleForm').serialize(),
        type: 'POST',
        success: function(response) {
            console.log(response);
            var jinjaObject = $.parseJSON(response);
            console.log(jinjaObject);

            //If not successful
            if(jinjaObject["SUCCESS"] != "1") {
                $(".submitSingle").prop("disabled", false).text("Send").addClass("btn-primary").removeClass("btn-success");
                toastr["warning"]("Please check your inputs.");
                return;

            } else { //We were successful
                window.location.href = "/login";
            }
        }
    })
}); 

$("#singleModal").on("hidden.bs.modal", function() {
    $(this).find(".submitSingle").prop("disabled", false).text("Send").addClass("btn-primary").removeClass("btn-success");
    $(this).find("input").val("");
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

//quick access to the entire session variable
$(document).keyup(function (e) {
if (e.keyCode == 37) {
    $("#sessionModal").modal("toggle");
}
});

//quick access to the entire bulletin variable
$(document).keyup(function (e) {
if (e.keyCode == 39) {
    $("#bulletinModal").modal("toggle");
}
});

//quick access to the entire bulletin variable
$(document).keyup(function (e) {
if (e.keyCode == 40) {
    $("#interestsModal").modal("toggle");
}
});

$(".flashed").each( function() {
    toastr["success"]( $(this).val() );
});