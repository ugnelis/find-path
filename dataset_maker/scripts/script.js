(function (window) {
    var canvas = this.__canvas = new fabric.Canvas('canvas', {selection: false});
    var polygon = new Polygon(canvas);

    var addMode = false;
    var editMode = false;

    var addButton = document.getElementById("add");
    var editButton = document.getElementById("edit");
    var myFieldset = document.getElementById("myFieldset");

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

    function saveData() {
        var value = document.querySelector('input[name="type"]:checked').value;
        polygon.saveData(value);
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

    myFieldset.disabled = true;
    window.newPolygon = newPolygon;
    window.saveData = saveData;
    window.editData = editData;
    window.removeData = removeData;

})(window);
