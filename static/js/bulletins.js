$(".addComment").on("click", function() {
	var data = {};
	data["studentID"] = $(this).attr("person");
	data["studentComment"] = $(this).closest(".input-group").find("input").val();
	data["articleID"] = $(this).attr("artID");

    $.ajax({
        url: '/studentBulletins/comment/' + $("#hiddenOrg").val(),
        data: data,
        type: 'POST',
        success: function(response) {
            var builder = $.parseJSON( response );
            if( builder["success"] == "0" ) {
            	toastr.clear();
            	toastr["warning"]("Sorry, we can't post that message");
            } else {//successfully

            }
        }//end of success
    })



});