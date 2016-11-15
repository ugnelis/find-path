var AddMode = (function () {

    var parent = parent;
    var canvas;

    var points = [];
    var firstCircle;

    var polygonEnded = false;
    var polygonCreated = false;

    var polygon;

    var lines = [];
    var circles = [];


    function AddMode(parent, canvas) {
        this.parent = parent;
        this.canvas = canvas;
    }

    AddMode.prototype.eventObjectMoving = function (event) {
        var target = event.target;
        target.point.x = target.left;
        target.point.y = target.top;
        this.canvas.renderAll();
    };

    AddMode.prototype.eventMouseUp = function (event) {

        // If first circle is clicked
        if (firstCircle == event.target && firstCircle != null) {
            polygonEnded = true;
        }

        if (!polygonEnded) {
            // Get mouse pointer
            var pointer = this.canvas.getPointer(event.e);
            var x = pointer.x;
            var y = pointer.y;
            points.push({x: x, y: y});

            // Add line
            this.addLine();

            // Add circle
            if (points.length == 1) {
                firstCircle = Utility.makeCircle(points[points.length - 1]);
                firstCircle.setFill('green');
                circles.push(firstCircle);
                this.canvas.add(firstCircle);
            } else {
                var circle = Utility.makeCircle(points[points.length - 1]);
                circles.push(circle);
                this.canvas.add(circle);
            }
        }

        if (polygonEnded && !polygonCreated) {
            // Add line
            this.addLine(true);

            polygon = Utility.makePolygon(points);
            this.canvas.sendToBack(polygon);

            polygonCreated = true;

            Utility.makeSelectable(circles, true);

            Utility.remove(this.canvas, lines);
        }

        this.canvas.renderAll();
    };

    AddMode.prototype.eventMouseOver = function (event) {
        if (firstCircle == event.target) {

            event.target.setFill('red');
        }

        if (polygon == event.target) {
            event.target.setFill(Utility.setPolygonColor(polygon, true));
        }
        this.canvas.renderAll();
    };

    AddMode.prototype.eventMouseOut = function (event) {
        if (firstCircle == event.target) {
            event.target.setFill('green');
        }

        if (polygon == event.target) {
            event.target.setFill(Utility.setPolygonColor(polygon, false));
        }
        this.canvas.renderAll();
    };

    AddMode.prototype.doAfter = function () {
        // Add polygon to the list.
        this.parent.addPolygon(polygon);

        Utility.remove(this.canvas, circles);

        // Reset variables.
        points = [];
        firstCircle = null;

        polygonEnded = false;
        polygonCreated = false;

        polygon = null;

        lines = [];
        circles = [];

        this.canvas.renderAll();
    };

    AddMode.prototype.addLine = function (last) {
        if (points.length > 1) {
            var line;

            if (last) {
                line = Utility.makeLine([
                    points[points.length - 1].x,
                    points[points.length - 1].y,
                    points[0].x,
                    points[0].y
                ]);
            } else {
                line = Utility.makeLine([
                    points[points.length - 2].x,
                    points[points.length - 2].y,
                    points[points.length - 1].x,
                    points[points.length - 1].y,
                ]);
            }
            lines.push(line);

            this.canvas.sendBackwards(line);
        }
    };

    return AddMode;
}());
