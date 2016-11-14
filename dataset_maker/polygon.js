var Polygon = (function () {

    var canvas;

    var polygons = [];

    var state = '';

    var mode;

    function Polygon(canvas) {
        this.canvas = canvas;
        //mode = new AddMode(this, canvas);

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
        state = (add) ? 'add' : '';
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
        state = (edit) ? 'edit' : '';
        for (var i = 0; i < polygons.length; i++) {
            this.canvas.remove(polygons[i]);
        }
        polygons = [];
    };

    Polygon.prototype.addPolygon = function (polygon) {
        polygons.push(polygon);
    };

    return Polygon;
}());
