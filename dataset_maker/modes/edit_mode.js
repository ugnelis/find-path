var EditMode = (function () {

    var canvas;

    function EditMode(canvas) {
        this.canvas = canvas;
        var rect1 = new fabric.Rect({
            width: 200, height: 100, left: 0, top: 50, angle: 30,
            fill: 'rgba(255,0,0,0.5)'
        });
        this.canvas.add(rect1);
    }

    EditMode.prototype.eventObjectMoving = function (event) {
    };

    EditMode.prototype.eventMouseUp = function (event) {
    };

    EditMode.prototype.eventMouseOver = function (event) {
    };

    EditMode.prototype.eventMouseOut = function (event) {
    };

    EditMode.prototype.doAfter = function () {
    };

    return EditMode;
}());
