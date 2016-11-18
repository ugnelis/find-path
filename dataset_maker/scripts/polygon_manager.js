var PolygonManager = (function () {

    var canvas;

    var polygons = [];

    var state = '';

    var mode;

    function PolygonManager(canvas) {
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

    PolygonManager.prototype.addMode = function (add) {
        if (add) {
            state = 'add';
            mode = new AddMode(this, this.canvas);
        } else {
            state = '';
            mode.doAfter();
            mode = null;
        }
    };

    PolygonManager.prototype.editMode = function (edit) {
        if (edit) {
            state = 'add';
            mode = new EditMode(this, this.canvas);
        } else {
            state = '';
            mode.doAfter();
            mode = null;
        }
    };

    PolygonManager.prototype.getPolygons = function () {
        return polygons;
    };

    PolygonManager.prototype.addPolygon = function (polygon) {
        polygons.push(polygon);
    };

    PolygonManager.prototype.removePolygon = function () {
        mode.remove();
    };

    PolygonManager.prototype.set = function (data) {
        mode.set(data);
    };

    return PolygonManager;
}());
