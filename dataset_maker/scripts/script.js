(function (window) {
    var canvas = this.__canvas = new fabric.Canvas('canvas', {selection: false});
    var polygonManager = new PolygonManager(canvas);

    var addMode = false;
    var editMode = false;

    // Buttons
    var addButton = document.getElementById("add");
    var editButton = document.getElementById("edit");
    var openImageButton = document.getElementById('open-image');
    var openJsonButton = document.getElementById('open-json');
    var saveFileButton = document.getElementById('save-file');

    // Inputs
    var alphaInput = document.getElementById("alpha");
    var betaInput = document.getElementById("beta");
    var scaleInput = document.getElementById("scale");
    var fileNameInput = document.getElementById("fileName");

    // Fieldsets
    var fileFieldset = document.getElementById("fileFieldset");
    var controllerFieldset = document.getElementById("controllerFieldset");

    var minScale = 320;
    var maxScale = 600;

    var width;
    var height;

    function newPolygon() {
        if (addMode == false) {
            addMode = true;
            addButton.innerHTML = "Done";

            editButton.disabled = true;
            controllerFieldset.disabled = false;
        } else if (addMode == true) {
            addMode = false;
            addButton.innerHTML = "New Polygon";

            editButton.disabled = false;
            controllerFieldset.disabled = true;
        }
        polygonManager.addMode(addMode);
    }

    function setData() {
        var value = document.querySelector('input[name="type"]:checked').value;
        polygonManager.set({type: value});
    }

    function editData() {
        if (editMode == false) {
            editMode = true;
            editButton.innerHTML = "Done";

            addButton.disabled = true;
            controllerFieldset.disabled = false;

        } else if (editMode == true) {
            editMode = false;
            editButton.innerHTML = "Edit";

            addButton.disabled = false;
            controllerFieldset.disabled = true;
        }
        polygonManager.editMode(editMode);
    }

    function removeData() {
        polygonManager.removePolygon();
    }

    function handleImageSelect(object) {
        var file = object.files[0];

        // Only process image file.
        if (!file.type.match('image.*')) {
            return;
        }

        var reader = new FileReader();

        // Closure to capture the file information.
        reader.onload = (function (file) {
            return function (event) {
                var image = new Image();
                image.src = event.target.result;

                // Set canvas size as the image size.
                image.onload = function () {
                    canvas.setDimensions({width: this.width, height: this.height});
                    addButton.disabled = false;
                    editButton.disabled = false;
                    scaleInput.max = image.width;
                    fileNameInput.value = file.name.substr(0, file.name.lastIndexOf('.')); // remove file extension
                };

                canvas.setBackgroundImage(image.src, canvas.renderAll.bind(canvas), {
                    originX: 'left',
                    originY: 'top',
                    left: 0,
                    top: 0
                });
            };

        })(file);
        // Read in the image file as a data URL.
        reader.readAsDataURL(file);
    }

    function handleJsonSelect(object) {
        var file = object.files[0];

        // Only process image file.
        if (!file.type.match('application/json')) {
            return;
        }

        var reader = new FileReader();

        // Closure to capture the file information.
        reader.onload = (function (file) {
            return function (event) {
                var jsonObject = JSON.parse(event.target.result);
                setParameters(jsonObject);
                console.log(jsonObject);
            };
        })(file);
        // Read in the image file as a data URL.
        reader.readAsText(file);
    }

    function handleFileSave() {

        var polygons = polygonManager.getPolygons();
        var data = {};
        data.class = document.querySelector('input[name="class"]:checked').value;

        data.alpha = Number(alphaInput.value);
        data.beta = Number(betaInput.value);

        data.polygons = [];
        for (var i = 0; i < polygons.length; i++) {
            data.polygons.push({type: polygons[i].type, points: polygons[i].points});
        }

        var json = JSON.stringify(data);
        var jsonBlob = new Blob([json], {type: "application/json"});
        // Open Dialog for json
        saveAs(jsonBlob, fileNameInput.value + ".json");

        var scaledImage = canvas.backgroundImage.toDataURL({format: 'jpeg'});
        var base64image = scaledImage.replace(/^data:image\/(png|jpeg);base64,/, "");

        var binary = convertBinaryToUnicode(atob(base64image));
        var imageBlob = new Blob([binary], {type: 'image/jpeg'});
        // Open Dialog for image
        saveAs(imageBlob, fileNameInput.value + ".jpg");

        canvas.deactivateAll().renderAll();
    }

    function setParameters(object) {
        document.getElementById(object.class).checked = true;
        alphaInput.value = object.alpha;
        betaInput.value = object.beta;
        // ...
    }

    function convertBinaryToUnicode(binaryImage) {
        var length = binaryImage.length;
        var buffer = new ArrayBuffer(length);
        var array = new Uint8Array(buffer);
        for (var i = 0; i < length; i++) {
            array[i] = binaryImage.charCodeAt(i);
        }
        return buffer;
    }

    function scale() {
        width = scaleInput.value;
        height = width * canvas.height / canvas.width;

        resizeObjects(width, height);
        resizeCanvas(width, height);
    }

    function resizeCanvas(width, height) {
        canvas.backgroundImage.scaleToWidth(width);
        canvas.backgroundImage.scaleToHeight(height);
        canvas.setDimensions({width: width, height: height});
        canvas.renderAll();
    }

    function resizeObjects(width, height) {
        var polygons = polygonManager.getPolygons();

        for (var i = 0; i < polygons.length; i++) {
            var points = polygons[i].points;

            for (var j = 0; j < points.length; j++) {
                points[j].x = width * points[j].x / canvas.width;
                points[j].y = height * points[j].y / canvas.height;
            }
        }
        canvas.renderAll();
    }

    addButton.disabled = true;
    editButton.disabled = true;
    controllerFieldset.disabled = true;

    scaleInput.min = minScale;
    scaleInput.max = maxScale;

    window.newPolygon = newPolygon;
    window.setData = setData;
    window.editData = editData;
    window.removeData = removeData;
    window.handleImageSelect = handleImageSelect;
    window.handleJsonSelect = handleJsonSelect;
    window.handleFileSave = handleFileSave;
    window.scale = scale;

})(window);
