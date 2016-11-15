var Polygon = (function () {

    var canvas;

    var polygons = [];

    var state = '';

    var mode;

    function Polygon(canvas) {
        this.canvas = canvas;

        this.canvas.on('object:moving', function (event) {
            mode.eventObjectMoving(event);
        });

        this.canvas.on('mouse:up', function (event) {
            mode.eventMouseUp(event);
        });

        this.canvas.on('mouse:over', function (event) {
            mode.eventMouseOver(event);
        });

        this.canvas.on('mouse:out', function (event) {
            mode.eventMouseOut(event);
        });
    }

    Polygon.prototype.addMode = function (add) {
        if (add) {
            state = 'add';
            mode = new AddMode(this, this.canvas);
        } else {
            state = '';
            mode.doAfter();
            mode = null;
        }
    };

    Polygon.prototype.editMode = function (edit) {
        if (edit) {
            state = 'add';
            mode = new EditMode(this, this.canvas);
        } else {
            state = '';
            mode.doAfter();
            mode = null;
        }
    };

    Polygon.prototype.getPolygons = function () {
        return polygons;
    };

    Polygon.prototype.addPolygon = function (polygon) {
        polygons.push(polygon);
    };

    Polygon.prototype.removePolygon = function () {
        mode.remove();
    };

    Polygon.prototype.set = function (data) {
        mode.set(data);
    };

    return Polygon;
}());
