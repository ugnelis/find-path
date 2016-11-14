var Polygon = (function () {

    var canvas;

    var points = [];
    var firstCircle;

    var polygonEnded = false;
    var polygonCreated = false;

    var polygon;
    var polygons = [];

    var lines = [];
    var circles = [];

    var state = '';

    function Polygon(canvas) {
        this.canvas = canvas;

        // Canvas events.
        var self = this;

        this.canvas.on('object:moving', function (event) {
            var target = event.target;
            target.point.x = target.left;
            target.point.y = target.top;
            canvas.renderAll();
        });

        this.canvas.on('mouse:up', function (event) {
            // If first circle is clicked
            if (firstCircle == event.target && firstCircle != null) {
                polygonEnded = true;
            }

            if (!polygonEnded) {
                // Get mouse pointer
                var pointer = canvas.getPointer(event.e);
                var x = pointer.x;
                var y = pointer.y;
                points.push({x: x, y: y});

                // Add line
                self.addLine();

                // Add circle
                if (points.length == 1) {
                    firstCircle = self.makeCircle(points[points.length - 1]);
                    firstCircle.setFill('green');
                    circles.push(firstCircle);
                    canvas.add(firstCircle);
                } else {
                    var circle = self.makeCircle(points[points.length - 1]);
                    circles.push(circle);
                    canvas.add(circle);
                }
            }

            if (polygonEnded && !polygonCreated) {
                // Add line
                self.addLine(true);

                polygon = self.makePolygon(points);
                canvas.sendToBack(polygon);

                polygonCreated = true;

                self.makeSelectable(circles, true);

                self.removeLines();
            }

            canvas.renderAll();
        });

        this.canvas.on('mouse:over', function (event) {
            if (firstCircle == event.target) {

                event.target.setFill('red');
            }

            if (polygon == event.target) {
                event.target.setFill(self.setPolygonColor(polygon, true));
            }
            canvas.renderAll();
        });

        this.canvas.on('mouse:out', function (event) {
            if (firstCircle == event.target) {
                event.target.setFill('green');
            }

            if (polygon == event.target) {
                event.target.setFill(self.setPolygonColor(polygon, false));
            }
            canvas.renderAll();
        });
    }

    Polygon.prototype.setPolygonColor = function (polygon, hover) {
        if (polygon.type == 'none') {
            return (hover) ? 'rgba(128, 0, 128, 1)' : 'rgba(128, 0, 128, 0.5)';
        }

        if (polygon.type == 'good') {
            return (hover) ? 'rgba(0, 153, 76, 1)' : 'rgba(0, 153, 76, 0.5)';
        }

        if (polygon.type == 'bad') {
            return (hover) ? 'rgba(204, 0, 0, 1)' : 'rgba(204, 0, 0, 0.5)';
        }
    };

    Polygon.prototype.makeCircle = function (point) {
        var circle = new fabric.Circle({
            left: point.x,
            top: point.y,
            strokeWidth: 5,
            radius: 12,
            fill: '#fff',
            stroke: '#666',
            selectable: false
        });
        circle.hasControls = false;
        circle.hasBorders = false;

        circle.originX = 'center';
        circle.originY = 'center';

        circle.point = point;
        return circle;
    };

    Polygon.prototype.makeLine = function (coords) {
        return new fabric.Line(coords, {
            fill: 'red',
            stroke: 'red',
            strokeWidth: 5,
            selectable: false
        });
    };

    Polygon.prototype.makePolygon = function (coords) {
        var polygon = new fabric.Polygon(coords, {
            selectable: false
        });
        polygon.type = 'none';
        //polygon.setFill('rgba(128, 0, 128, 0.5)');
        polygon.setFill(this.setPolygonColor(polygon));

        return polygon;
    };

    Polygon.prototype.generateLines = function (points) {
        var lines = [];
        var line = this.makeLine([
            points[points.length - 1].x,
            points[points.length - 1].y,
            points[0].x,
            points[0].y
        ]);
        lines.push(line);

        for (var i = 0; i < points.length - 1; i++) {
            line = this.makeLine([
                points[i].x,
                points[i].y,
                points[i + 1].x,
                points[i + 1].y
            ]);
            lines.push(line);
        }

        return lines;
    };

    Polygon.prototype.generateCircles = function (points) {
        var circles = [];

        for (var i = 0; i < points.length; i++) {
            var circle = this.makeCircle(points[i]);
            circles.push(circle);
        }

        return circles;
    };

    Polygon.prototype.drawElements = function (elements) {
        for (var i = 0; i < elements.length; i++) {
            this.canvas.add(elements[i]);
        }
    };

    Polygon.prototype.addPolygon = function () {
        polygon = this.makePolygon(points);
        this.canvas.sendToBack(polygon);
    };

    Polygon.prototype.addLine = function (last) {
        if (points.length > 1) {
            var line;

            if (last) {
                line = this.makeLine([
                    points[points.length - 1].x,
                    points[points.length - 1].y,
                    points[0].x,
                    points[0].y
                ]);
            } else {
                line = this.makeLine([
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

    Polygon.prototype.removeLines = function () {
        for (var i = 0; i < lines.length; i++) {
            this.canvas.remove(lines[i]);
        }
        lines = [];
    };

    Polygon.prototype.removeCircles = function () {
        for (var i = 0; i < circles.length; i++) {
            this.canvas.remove(circles[i]);
        }
        circles = [];
    };

    Polygon.prototype.makeSelectable = function (object, value) {
        if (Array.isArray(object)) {
            for (var i = 0; i < object.length; i++) {
                object[i].selectable = value;
            }
        } else {
            object.selectable = true;
        }
    };

    Polygon.prototype.refresh = function () {
        polygon.setFill(this.setPolygonColor(polygon));
        this.canvas.renderAll();
    };

    Polygon.prototype.saveData = function (type) {
        if (type == 'good') {
            polygon.type = 'good';
        }

        if (type == 'bad') {
            polygon.type = 'bad';
        }

        this.refresh();
    };

    Polygon.prototype.doBeforeState = function () {
        if (state == 'add') {
            // Add polygon to the list.
            polygons.push(polygon);

            this.removeCircles();

            // Reset variables.
            points = [];
            firstCircle = null;

            polygonEnded = false;
            polygonCreated = false;

            polygon = null;
        }

        if (state == 'edit') {
        }
    };

    Polygon.prototype.doOnState = function () {
        if (state == 'add') {
            // Add polygon to the list.
            polygons.push(polygon);

            this.removeCircles();

            // Reset variables.
            points = [];
            firstCircle = null;

            polygonEnded = false;
            polygonCreated = false;

            polygon = null;
        }

        if (state == 'edit') {
        }
    };

    Polygon.prototype.newPolygon = function (add) {
        state = (add) ? 'add' : '';
        this.doOnState();
    };

    Polygon.prototype.editMode = function (edit) {
        state = (edit) ? 'edit' : '';
        this.doOnState();
    };

    return Polygon;
}());
