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

        if (target.left < 0)
            target.left = 0;

        if (target.left > this.canvas.getWidth())
            target.left = this.canvas.getWidth();

        if (target.top < 0)
            target.top = 0;

        if (target.top > this.canvas.getHeight())
            target.top = this.canvas.getHeight();

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
                Utility.add(this.canvas, firstCircle);
            } else {
                var circle = Utility.makeCircle(points[points.length - 1]);
                circles.push(circle);
                Utility.add(this.canvas, circle);
            }
        }

        if (polygonEnded && !polygonCreated) {
            // Add line
            this.addLine(true);

            polygon = Utility.makePolygon(points);
            Utility.add(this.canvas, polygon);
            Utility.bringToFront(this.canvas, circles);

            polygonCreated = true;

            Utility.makeSelectable(circles, true);

            Utility.remove(this.canvas, lines);
        }

        this.canvas.renderAll();
    };

    AddMode.prototype.eventMouseOver = function (event) {
        if (firstCircle == event.target) {
            event.target.setFill('rgba(0, 0, 204, 0.8)');
        }

        if (polygon == event.target) {
            event.target.setFill(Utility.setPolygonColor(polygon, true));
        }
        this.canvas.renderAll();
    };

    AddMode.prototype.eventMouseOut = function (event) {
        if (firstCircle == event.target) {
            event.target.setFill('rgba(0, 0, 204, 0.5)');
        }

        if (polygon == event.target) {
            event.target.setFill(Utility.setPolygonColor(polygon, false));
        }
        this.canvas.renderAll();
    };

    AddMode.prototype.doAfter = function () {
        // Add polygon to the list.
        if (polygon != null) {
            this.parent.addPolygon(polygon);
        }

        Utility.remove(this.canvas, lines);
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

    AddMode.prototype.remove = function () {
        Utility.remove(this.canvas, lines);
        Utility.remove(this.canvas, circles);
        Utility.remove(this.canvas, polygon);

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

    AddMode.prototype.set = function (options) {
        if (polygon != null) {
            polygon.type = options.type;
            polygon.setFill(Utility.setPolygonColor(polygon, false));
            this.canvas.renderAll();
        }
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

            Utility.add(this.canvas, line);

            // Bring circles to front in canvas.
            Utility.bringToFront(this.canvas, circles)
        }
    };

    return AddMode;
}());
