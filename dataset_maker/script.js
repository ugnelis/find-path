(function (window) {

    // var points = [
    //     {x: 250, y: 125},
    //     {x: 175, y: 225},
    //     {x: 200, y: 350},
    //     {x: 300, y: 350},
    //     {x: 325, y: 225}
    // ];

    var points = [];

    var canvas = this.__canvas = new fabric.Canvas('canvas', {selection: false});

    function makeCircle(point) {
        var c = new fabric.Circle({
            left: point.x,
            top: point.y,
            strokeWidth: 5,
            radius: 12,
            fill: '#fff',
            stroke: '#666'
        });
        c.hasControls = c.hasBorders = false;

        c.originX = c.originY = 'center';

        c.point = point;
        return c;
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

    canvas.on('object:moving', function (event) {
        var p = event.target;
        p.point.x = p.left;
        p.point.y = p.top;
        canvas.renderAll();
    });

    canvas.on('mouse:up', function (event) {
        // TODO remove if
        if (points.length < 10) {
            var pointer = canvas.getPointer(event.e);
            var x = pointer.x;
            var y = pointer.y;
            points.push({x: x, y: y});
            var circle = makeCircle(points[points.length - 1]);
            canvas.add(circle);
        }

        canvas.renderAll();
    });

    window.addPolygon = addPolygon;

})
(window);


