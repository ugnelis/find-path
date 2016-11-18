(function (window) {
    var canvas = this.__canvas = new fabric.Canvas('canvas', {selection: false});
    var polygon = new Polygon(canvas);

    var addMode = false;
    var editMode = false;

    var addButton = document.getElementById("add");
    var editButton = document.getElementById("edit");
    var myFieldset = document.getElementById("myFieldset");
    var file = document.getElementById('file');

    function newPolygon() {
        if (addMode == false) {
            addMode = true;
            addButton.innerHTML = "Done";

            editButton.disabled = true;
            myFieldset.disabled = false;
        } else if (addMode == true) {
            addMode = false;
            addButton.innerHTML = "New Polygon";

            editButton.disabled = false;
            myFieldset.disabled = true;
        }
        polygon.addMode(addMode);
    }

    function setData() {
        var value = document.querySelector('input[name="type"]:checked').value;
        polygon.set({type: value});
    }

    function editData() {
        if (editMode == false) {
            editMode = true;
            editButton.innerHTML = "Done";

            addButton.disabled = true;
            myFieldset.disabled = false;

        } else if (editMode == true) {
            editMode = false;
            editButton.innerHTML = "Edit";

            addButton.disabled = false;
            myFieldset.disabled = true;
        }
        polygon.editMode(editMode);
    }

    function removeData() {
        polygon.removePolygon();
    }

    function handleFileSelect(object) {
        var file = object.files[0];

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

    addButton.disabled = true;
    editButton.disabled = true;
    myFieldset.disabled = true;
    window.newPolygon = newPolygon;
    window.setData = setData;
    window.editData = editData;
    window.removeData = removeData;
    window.handleFileSelect = handleFileSelect;

})(window);
