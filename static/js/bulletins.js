$(".addComment").on("click", function() {
	var data = {};
	data["studentID"] = $(this).attr("person");
	data["studentComment"] = $(this).closest(".input-group").find("input").val();
	data["articleID"] = $(this).attr("artID");
	$(this).closest(".input-group").find("input").val("");

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
								"<p class='chatBlue well text-right'>" +
									"<span class='pull-left'>" +
										$(".grabAndGo").text().replace(/ /g,'') +
									"says... </span> "+
									data["studentComment"] +
								"</p>" +
							"</div>";



			// console.log($(".grabAndGo").text().replace(/ /g,''));
			$(".chat[artID='"+ data["articleID"] +"']").append(chatToss);
            


            }
        }//end of success
    })



});