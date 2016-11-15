var EditMode = (function () {

    var parent = parent;
    var canvas;

    var polygons;
    var selectedPolygon;

    function EditMode(parent, canvas) {
        this.parent = parent;
        this.canvas = canvas;

        polygons = this.parent.getPolygons();
        console.log(polygons);
    }

    EditMode.prototype.eventObjectMoving = function (event) {
    };

    EditMode.prototype.eventMouseUp = function (event) {
    };

    EditMode.prototype.eventMouseOver = function (event) {
    };

    EditMode.prototype.eventMouseOut = function (event) {
    };

    EditMode.prototype.doAfter = function () {
    };

    return EditMode;
}());
