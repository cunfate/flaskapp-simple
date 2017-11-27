var handler = {
	init: function(container) {
		container.on("dragover", function(event){
			event.preventDefault();
		});
		container.on("drop", function(event){
			event.preventDefault();
			var file = event.originalEvent.dataTransfer.files[0];
			handler.handleDrop($(this), file);
		})
	}
};

var readImgFile = function(file, img, container) {
	var reader = new FileReader(file);
	if(file.type.split("/")[0] !== "image") {
		return;
	}

	reader.onLoad = function(event) {
		var base64 = event.target.result;
		img.attr("src", baseUrl);
		handler.compressAndUpload(img, base64, file, container);
	}

	reader.readAsDataURL(file);
}

// function to preview image
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
		document.getElementById("upLoadShow").src = event.target.result;
	}
	oFReader.readAsDataURL(oFile);
}

var showImageCropperModelBox = function() {
	
}
