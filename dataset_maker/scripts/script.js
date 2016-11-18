(function (window) {
    var canvas = this.__canvas = new fabric.Canvas('canvas', {selection: false});
    var polygonManager = new PolygonManager(canvas);

    var addMode = false;
    var editMode = false;

    // Buttons
    var addButton = document.getElementById("add");
    var editButton = document.getElementById("edit");
    var openFileButton = document.getElementById('open-file');
    var saveFileButton = document.getElementById('save-file');

    // Inputs
    var alphaInput = document.getElementById("alpha");
    var betaInput = document.getElementById("beta");

    // Fieldsets
    var fileFieldset = document.getElementById("fileFieldset");
    var controllerFieldset = document.getElementById("controllerFieldset");


    var file; // Image file;

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

    function handleFileSelect(object) {
        file = object.files[0];

        // Only process image file.
        if (!file.type.match('image.*')) {
            return;
        }

        var reader = new FileReader();

        // Closure to capture the file information.
        reader.onload = (function (theFile) {
            return function (event) {
                var image = new Image();
                image.src = event.target.result;

                // Set canvas size as the image size.
                image.onload = function () {
                    canvas.setDimensions({width: this.width, height: this.height});
                    addButton.disabled = false;
                    editButton.disabled = false;
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
        var blob = new Blob([json], {type: "application/json"});
        var url = URL.createObjectURL(blob);
        saveAs(blob, file.name + ".json");
    }

    addButton.disabled = true;
    editButton.disabled = true;
    controllerFieldset.disabled = true;
    window.newPolygon = newPolygon;
    window.setData = setData;
    window.editData = editData;
    window.removeData = removeData;
    window.handleFileSelect = handleFileSelect;
    window.handleFileSave = handleFileSave;

})(window);
