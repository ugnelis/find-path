var Polygon = (function () {

    var canvas;

    var points = [];
    var firstCircle;

    var polygonEnded = false;
    var polygonCreated = false;

    var polygon;
    var lines = [];

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
            // if clicked first circle;
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
                    canvas.add(firstCircle);
                } else {

                    var circle = self.makeCircle(points[points.length - 1]);
                    canvas.add(circle);
                }
            }

            if (polygonEnded && !polygonCreated) {
                // Add line
                self.addLine(true);

                polygon = self.makePolygon(points);
                canvas.sendToBack(polygon);

                polygonCreated = true;

                self.removeLines();
            }

            canvas.renderAll();
        });

        this.canvas.on('mouse:over', function (event) {
            if (firstCircle == event.target) {

                event.target.setFill('red');
            }

            if (polygon == event.target) {
                event.target.setFill('rgba(128, 0, 128, 1)');
            }
            canvas.renderAll();
        });

        this.canvas.on('mouse:out', function (event) {
            if (firstCircle == event.target) {
                event.target.setFill('green');
            }

            if (polygon == event.target) {
                event.target.setFill('rgba(128, 0, 128, 0.5)');
            }
            canvas.renderAll();
        });
    }

    Polygon.prototype.makeCircle = function (point) {
        var circle = new fabric.Circle({
            left: point.x,
            top: point.y,
            strokeWidth: 5,
            radius: 12,
            fill: '#fff',
            stroke: '#666'
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
        return new fabric.Polygon(coords, {
            fill: 'rgba(128, 0, 128, 0.5)',
            selectable: false
        });
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
        this.polygon = this.makePolygon(this.points);
        this.canvas.sendToBack(this.polygon);
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

            this.canvas.sendToBack(line);
        }
    };

    Polygon.prototype.removeLines = function () {
        for (var i = 0; i < lines.length; i++) {
            this.canvas.remove(lines[i]);
        }
        lines = [];
    };

    return Polygon;
}());