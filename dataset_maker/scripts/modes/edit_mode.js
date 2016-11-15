var EditMode = (function () {

    var parent = parent;
    var canvas;

    var polygons;

    var selectedPolygon;
    var isSelected = false;

    var circles = [];

    function EditMode(parent, canvas) {
        this.parent = parent;
        this.canvas = canvas;

        polygons = this.parent.getPolygons();
    }

    EditMode.prototype.eventObjectMoving = function (event) {
        var target = event.target;
        target.point.x = target.left;
        target.point.y = target.top;
        this.canvas.renderAll();
    };

    EditMode.prototype.eventMouseUp = function (event) {
        if (selectedPolygon != null && !isSelected) {
            isSelected = true;

            // Reset color.
            selectedPolygon.setFill(Utility.setPolygonColor(selectedPolygon, false));

            // Generate circles and make them selectable.
            circles = Utility.generateCircles(selectedPolygon.points);
            Utility.add(this.canvas, circles);
            Utility.makeSelectable(circles, true);
        }
    };

    EditMode.prototype.eventMouseOver = function (event) {
        if (!isSelected) {
            for (var i = 0; i < polygons.length; i++) {
                if (polygons[i] == event.target) {
                    event.target.setFill(Utility.setPolygonColor(polygons[i], true));
                    selectedPolygon = polygons[i];
                }
            }
        }
        this.canvas.renderAll();
    };

    EditMode.prototype.eventMouseOut = function (event) {
        if (!isSelected) {
            for (var i = 0; i < polygons.length; i++) {
                if (polygons[i] == event.target) {
                    event.target.setFill(Utility.setPolygonColor(polygons[i], false));
                }
            }
        }
        this.canvas.renderAll();
    };

    EditMode.prototype.doAfter = function () {
        Utility.remove(this.canvas, circles);

        selectedPolygon = null;
        isSelected = false;

        circles = [];

        this.canvas.renderAll();
    };

    EditMode.prototype.remove = function () {
        Utility.remove(this.canvas, selectedPolygon);
        Utility.remove(this.canvas, circles);

        selectedPolygon = null;
        isSelected = false;

        circles = [];

        this.canvas.renderAll();
    };

    EditMode.prototype.set = function (options) {
        if (selectedPolygon != null) {
            selectedPolygon.type = options.type;
            selectedPolygon.setFill(Utility.setPolygonColor(selectedPolygon, false));
            this.canvas.renderAll();
        }
    };

    return EditMode;
}());
