jQuery(function($){
    // The variable jcrop_api will hold a reference to the
    // Jcrop API once Jcrop is instantiated.
    var jcrop_api;

    // In this example, since Jcrop may be attached or detached
    // at the whim of the user, I've wrapped the call into a function
    initJcrop();
    
    // The function is pretty simple
    function initJcrop()//
    {
      // Hide any interface elements that require Jcrop
      // (This is for the local user interface portion.)
      //$('.requiresjcrop').hide();

      // Invoke Jcrop in typical fashion
      $('#avatar_upload').Jcrop({
        onRelease: releaseCheck
      },function(){

        jcrop_api = this;
        jcrop_api.animateTo([0,0,100,100]);
		//Set the resize function disable.
      	jcrop_api.setOptions({ allowResize: false });
      	jcrop_api.focus();

        // Setup and dipslay the interface for "enabled"
        // Setup and dipslay the interface for "enabled"
        //$('#can_click,#can_move,#can_size').attr('checked','checked');
        //$('#ar_lock,#size_lock,#bg_swap').attr('checked',false);
        //$('.requiresjcrop').show();

      });

    }

	function getSelect()
	{
		return jcrop_api.tellSelect();
	}

	$(".btn-upfile").onClick(function() {
		var formData = new FormData();
		formData.append('file', $("#file")[0].files[0]);
		$.ajax({
		url: "avatar",
		type: "POST",
		cache: false,
		data: formData,
		processData: false,
		contentType: false
		}).done(function(res){
			before_path = $('#avatar_upload').attr("src");
			after_path = before_path + "?t=&" + Math.random();
			$('#avatar_upload').attr('src', after_path);
		}).fail(function(res){
		})
	});

	$("#btn-confirm-crop").onClick(
			function() {
				var selection = jcrop_api.tellSelect();
				$.ajax({
					url: "avatarcrop",
					type: "POST",
					data: JSON.stringify(selection),
					contentType: 'application/json; charset=utf-8',
					dataType: 'json',
					async: false
				}).done(function(res){
					before_path = $('#avatar_upload').attr("src");
					after_path = before_path + "?t=&" + Math.random();
					$('#avatar_upload').attr('src', after_path);
				}).fail(function(res){
				});
			}
			)
}
