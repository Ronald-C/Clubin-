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
            } else {//successfully can make comment
                        
          	 var chatToss = "<div class='item'>" +
							"<img src='{{ url_for('static', filename='dist/img/spartan.jpg') }}' alt='user image' class='online'>" +
							"<p class='message'>" +
							data["studentComment"] +
							"</p>" +
							"</div>"
			console.log("this is what I'm selecting");
			console.log($(".chat[artID='"+ data["articleID"] +"']"));			
			$(".chat[artID='"+ data["articleID"] +"']").append(chatToss);
            


            }
        }//end of success
    })



});