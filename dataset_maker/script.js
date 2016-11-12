(function () {
    var points = [
        {x: 250, y: 125},
        {x: 175, y: 225},
        {x: 200, y: 350},
        {x: 300, y: 350},
        {x: 325, y: 225}
    ];

    var canvas = this.__canvas = new fabric.Canvas('canvas', {selection: false});
    //fabric.Object.prototype.originX = fabric.Object.prototype.originY = 'center';

    /*function makeCircle(left, top, line1, line2) {
        var c = new fabric.Circle({
            left: left,
            top: top,
            strokeWidth: 5,
            radius: 12,
            fill: '#fff',
            stroke: '#666'
        });
        c.hasControls = c.hasBorders = false;

        c.line1 = line1;
        c.line2 = line2;

        return c;
    }*/

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
            fill: 'purple',
            selectable: true
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

    /*function generateCircles(lines) {
        console.log(lines);
        var circles = [];

        var circle = makeCircle(lines[0].get('x1'), lines[0].get('y1'), lines[points.length - 1], lines[0]);
        circles.push(circle);

        for (var i = 0; i < lines.length - 1; i++) {
            circle = makeCircle(lines[i].get('x1'), lines[i].get('y1'), lines[i], lines[i+1]);
            circles.push(circle);
        }

        return circles;
    }*/

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

    var lines = generateLines(points);
    var circles = generateCircles(points);

    drawElements(lines);
    drawElements(circles);

    console.log(circles);

    // var line1 = makeLine([250, 125, 175, 225]),
    //     line2 = makeLine([175, 225, 200, 350]),
    //     line3 = makeLine([200, 350, 300, 350]),
    //     line4 = makeLine([300, 350, 325, 225]),
    //     line5 = makeLine([325, 225, 250, 125]);
    //
    // canvas.add(line1, line2, line3, line4, line5);

    // canvas.add(
    //     makeCircle(line1.get('x1'), line1.get('y1'), line5, line1),
    //     makeCircle(line2.get('x1'), line2.get('y1'), line1, line2),
    //     makeCircle(line3.get('x1'), line3.get('y1'), line2, line3),
    //     makeCircle(line4.get('x1'), line4.get('y1'), line3, line4),
    //     makeCircle(line5.get('x1'), line5.get('y1'), line4, line5)
    // );


    canvas.on('object:moving', function (e) {
        var p = e.target;
        //p.line1 && p.line1.set({'x2': p.left, 'y2': p.top});
        //p.line2 && p.line2.set({'x1': p.left, 'y1': p.top});
        p.point.x = p.left;
        p.point.y = p.top;
        canvas.renderAll();
    });


    //canvas.add(makeCircle(points[0], polygon));

})();


