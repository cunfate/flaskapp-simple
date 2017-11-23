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
var loadImageFile() {
	if(document.getElementById("uploadimageinput").files.length === 0) return;
	var oFile = document.getElementById("uploadimageinput").files[0];
	//test file types like:
	//if(!fileFilter.test(oFile.type)) {alter("You must select a valid image file");}
	oFReader = new FileReader();
	oFReader.onload = function(event) {
		//2 bit image src code
		document.getElementById("uploadimageshow").src = event.target.result;
	}
	oFReader.readAsDataURL(oFile);
}
