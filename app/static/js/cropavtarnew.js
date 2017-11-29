// function to preview images
var loadImageFile = function() {
	var rFilter = /^(?:image\/bmp|image\/cis\-cod|image\/gif|image\/ief|image\/jpeg|image\/jpeg|image\/jpeg|image\/pipeg|image\/png|image\/svg\+xml|image\/tiff|image\/x\-cmu\-raster|image\/x\-cmx|image\/x\-icon|image\/x\-portable\-anymap|image\/x\-portable\-bitmap|image\/x\-portable\-graymap|image\/x\-portable\-pixmap|image\/x\-rgb|image\/x\-xbitmap|image\/x\-xpixmap|image\/x\-xwindowdump)$/i;
	inputFile = document.getElementById("avatar");
	if(inputFile.files.length === 0) return;
	var oFile = inputFile.files[0];
	//test file types like:
	if(!rFilter.test(oFile.type)) {
		alter("You must select a valid image file"); 
		return;
	}
	oFReader = new FileReader();
	oFReader.onload = function(event) {
		//bin code image src code
		console.log('load ok!');
		document.getElementById("upLoadShow").src = event.target.result;
		$("#upLoadShow").attr("style", "");
	}
	oFReader.readAsDataURL(oFile);
};

var initCropper = function() {
	var jcrop_api_crop = null;
	var initJcrop = function() {
	  $('#upLoadShow').hide();

      // Invoke Jcrop in typical fashion
      $('#upLoadShow').Jcrop({
        onRelease: releaseCheck,
      },function(){
        	jcrop_api_crop = this;
        	jcrop_api_crop.animateTo([0,0,100,100]);
			//Set the resize function disable.
      		jcrop_api_crop.setOptions({ allowResize: false });
      		jcrop_api_crop.setOptions({ allowMove: true});
			jcrop_api_crop.setOptions({ allowSelect: false });
      		jcrop_api_crop.focus();

			$('#upLoadShow').show();
		});
	};

	initJcrop();

	jcrop_api_crop.enable();
	function releaseCheck(){};

	function getSelect()
	{
		return jcrop_api_crop.tellSelect();
	}

	$("#submitCropper").on("click", function(){
		var formData = new FormData();
		var area = JSON.stringify(getSelect());
		formData.append('file', $("#avatar")[0].files[0]);
		formData.append('area', area);
		$.ajax({
		url: "avatarnew",
		type: "POST",
		cache: false,
		data: formData,
		//dataType: "multipart/form-data",
		dataType:"json",
		processData: false,
		contentType: false
		}).success(function(res, code, obj){
			console.log(res);
			$("#cropModal").modal("hide");
			$("#upsuccess-block").removeClass("hide");
			//$('<div class="alert alert-success role="alert">Upload avatar success!</div>').insertBefore("#avatar_upload");
		}).error(function(res, code, obj){
			console.log('something error!');
			console.log(res);
			console.log(res.responseText);
			console.log(code);
		});
	});
};
