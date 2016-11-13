(function (window) {

    var points = [];
    var firstCircle;

    var polygonEnded = false;
    var polygonCreated = false;

    var lines = [];

    var canvas = this.__canvas = new fabric.Canvas('canvas', {selection: false});

    function makeCircle(point) {
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
    }

    function makeLine(coords) {
        return new fabric.Line(coords, {
            fill: 'red',
            stroke: 'red',
            strokeWidth: 5,
            selectable: false
        });
    }

    function makePolygon(coords) {
        return new fabric.Polygon(coords, {
            fill: 'rgba(128, 0, 128, 0.5)',
            selectable: false
        });
    }

    function generateLines(points) {
        var lines = [];

        var line = makeLine([
            points[points.length - 1].x,
            points[points.length - 1].y,
            points[0].x,
            points[0].y
        ]);
        lines.push(line);

        for (var i = 0; i < points.length - 1; i++) {
            line = makeLine([
                points[i].x,
                points[i].y,
                points[i + 1].x,
                points[i + 1].y
            ]);
            lines.push(line);
        }

        return lines;
    }

    function generateCircles(points) {
        var circles = [];

        for (var i = 0; i < points.length; i++) {
            var circle = makeCircle(points[i]);
            circles.push(circle);
        }

        return circles;
    }

    function drawElements(elements) {
        for (var i = 0; i < elements.length; i++) {
            canvas.add(elements[i]);
        }
    }

    var polygon = makePolygon(points);
    canvas.add(polygon);

    //var lines = generateLines(points);
    var circles = generateCircles(points);

    //drawElements(lines);
    drawElements(circles);


    function addPolygon() {
        var polygon = makePolygon(points);
        canvas.sendToBack(polygon);
        canvas.renderAll();
    }

    function addLine(last) {
        if (points.length > 1) {
            var line;

            if (last) {
                line = makeLine([
                    points[points.length - 1].x,
                    points[points.length - 1].y,
                    points[0].x,
                    points[0].y
                ]);
            } else {
                line = makeLine([
                    points[points.length - 2].x,
                    points[points.length - 2].y,
                    points[points.length - 1].x,
                    points[points.length - 1].y,
                ]);
            }
            lines.push(line);
            canvas.sendToBack(line);
        }
    }

    function removeLines() {
        for (var i = 0; i < lines.length; i++) {
            canvas.remove(lines[i]);
        }
    }


    canvas.on('object:moving', function (event) {
        var target = event.target;
        target.point.x = target.left;
        target.point.y = target.top;
        canvas.renderAll();
    });

    canvas.on('mouse:up', function (event) {
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
            addLine();

            // Add circle
            if (points.length == 1) {
                firstCircle = makeCircle(points[points.length - 1]);
                firstCircle.setFill('green');
                canvas.add(firstCircle);
            } else {
                var circle = makeCircle(points[points.length - 1]);
                canvas.add(circle);
            }
        }

        if (polygonEnded && !polygonCreated) {
            // Add line
            addLine(true);

            var polygon = makePolygon(points);
            canvas.sendToBack(polygon);

            polygonCreated = true;

            removeLines();
        }

        canvas.renderAll();
    });

    canvas.on('mouse:over', function (event) {
        if (firstCircle == event.target) {
            event.target.setFill('red');
        }
        canvas.renderAll();
    });

    canvas.on('mouse:out', function (event) {
        if (firstCircle == event.target) {
            event.target.setFill('green');
        }
        canvas.renderAll();
    });

    function test() {
        console.log("It works");
    }

    window.addPolygon = test;


})
(window);


