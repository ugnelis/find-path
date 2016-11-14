(function (window) {
    var canvas = this.__canvas = new fabric.Canvas('canvas', {selection: false});
    var polygon = new Polygon(canvas);

    var addMode = false;
    var editMode = false;

    function addPolygon() {
        if (addMode == false) {
            document.getElementById("add").innerHTML = "Done";
            addMode = true;
        } else if (addMode == true) {
            document.getElementById("add").innerHTML = "Add Polygon";
            addMode = false;
        }
        polygon.newPolygon(addMode);
    }

    function saveData() {
        var value = document.querySelector('input[name="type"]:checked').value;
        polygon.saveData(value);
    }

    function editData() {
        if (editMode == false) {
            document.getElementById("edit").innerHTML = "Done";
            editMode = true;
        } else if (editMode == true) {
            document.getElementById("edit").innerHTML = "Edit";
            editMode = false;
        }
        polygon.editMode(editMode);
    }

    window.addPolygon = addPolygon;
    window.saveData = saveData;
    window.editData = editData;

})(window);


