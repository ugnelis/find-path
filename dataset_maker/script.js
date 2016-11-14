(function (window) {
    var canvas = this.__canvas = new fabric.Canvas('canvas', {selection: false});

    console.log(canvas);
    var polygon = new Polygon(canvas);

    function test() {
        polygon.newPolygon();
    }

    window.addPolygon = test;
})(window);