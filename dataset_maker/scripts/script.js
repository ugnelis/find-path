(function (window) {
    var canvas = this.__canvas = new fabric.Canvas('canvas', {selection: false});
    var polygon = new Polygon(canvas);

    var addMode = false;
    var editMode = false;

    function newPolygon() {
        if (addMode == false) {
            document.getElementById("add").innerHTML = "Done";
            document.getElementById("edit").disabled = true;
            addMode = true;
        } else if (addMode == true) {
            document.getElementById("add").innerHTML = "New Polygon";
            document.getElementById("edit").disabled = false;
            addMode = false;
        }
        polygon.addMode(addMode);
    }

    function saveData() {
        var value = document.querySelector('input[name="type"]:checked').value;
        polygon.saveData(value);
    }

    function editData() {
        if (editMode == false) {
            document.getElementById("edit").innerHTML = "Done";
            document.getElementById("add").disabled = true;
            editMode = true;
        } else if (editMode == true) {
            document.getElementById("edit").innerHTML = "Edit";
            document.getElementById("add").disabled = false;
            editMode = false;
        }
        polygon.editMode(editMode);
    }

    window.newPolygon = newPolygon;
    window.saveData = saveData;
    window.editData = editData;

})(window);
