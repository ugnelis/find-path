(function (window) {
    var canvas = this.__canvas = new fabric.Canvas('canvas', {selection: false});

    console.log(canvas);
    var polygon = new Polygon(canvas);

    function test() {
        console.log("It works!");
    }

    window.addPolygon = test;
})(window);