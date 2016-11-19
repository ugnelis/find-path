var Utility = (function () {
    return {
        makeCircle: function (point) {
            var circle = new fabric.Circle({
                left: point.x,
                top: point.y,
                strokeWidth: 5,
                radius: 12,
                fill: '',
                stroke: '#666',
                selectable: false
            });
            circle.hasControls = false;
            circle.hasBorders = false;

            circle.originX = 'center';
            circle.originY = 'center';

            circle.point = point;
            return circle;
        },
        makeLine: function (coords) {
            return new fabric.Line(coords, {
                fill: 'red',
                stroke: 'red',
                strokeWidth: 3,
                selectable: false
            });
        },
        makePolygon: function (coords) {
            var polygon = new fabric.Polygon(coords, {
                selectable: false
            });
            polygon.type = 'none';
            polygon.setFill(this.setPolygonColor(polygon));

            return polygon;
        },
        setPolygonColor: function (polygon, hover) {
            if (polygon.type == 'none') {
                return (hover) ? 'rgba(255, 255, 255, 1)' : 'rgba(255, 255, 255, 0.5)';
            }

            if (polygon.type == 'route') {
                return (hover) ? 'rgba(0, 153, 76, 1)' : 'rgba(0, 153, 76, 0.5)';
            }

            if (polygon.type == 'boundary') {
                return (hover) ? 'rgba(204, 0, 0, 1)' : 'rgba(204, 0, 0, 0.5)';
            }

            if (polygon.type == 'obstacle') {
                return (hover) ? 'rgba(128, 0, 128, 1)' : 'rgba(128, 0, 128, 0.5)';
            }
        },
        makeSelectable: function (object, value) {
            if (Array.isArray(object)) {
                for (var i = 0; i < object.length; i++) {
                    object[i].selectable = value;
                }
            } else {
                object.selectable = value;
            }
        },
        generateCircles: function (points) {
            var circles = [];

            for (var i = 0; i < points.length; i++) {
                var circle = Utility.makeCircle(points[i]);
                circles.push(circle);
            }

            return circles;
        },
        add: function (canvas, object) {
            if (Array.isArray(object)) {
                for (var i = 0; i < object.length; i++) {
                    canvas.add(object[i]);
                }
            } else {
                canvas.add(object);
            }
        },
        bringToFront: function (canvas, object) {
            if (Array.isArray(object)) {
                for (var i = 0; i < object.length; i++) {
                    canvas.bringToFront(object[i]);
                }
            } else {
                canvas.bringToFront(object);
            }
        },
        bringToBack: function (canvas, object) {
            if (Array.isArray(object)) {
                for (var i = 0; i < object.length; i++) {
                    canvas.bringToBack(object[i]);
                }
            } else {
                canvas.bringToBack(object);
            }
        },
        remove: function (canvas, object) {
            if (Array.isArray(object)) {
                for (var i = 0; i < object.length; i++) {
                    canvas.remove(object[i]);
                }
                object = [];
            } else {
                canvas.remove(object);
                object = null;
            }
        }
    }
}());
