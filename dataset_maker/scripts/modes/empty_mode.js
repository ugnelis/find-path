var EmptyMode = (function () {

    var parent = parent;
    var canvas;

    function EmptyMode(parent, canvas) {
        this.parent = parent;
        this.canvas = canvas;
    }

    EmptyMode.prototype.eventObjectMoving = function (event) {
    };

    EmptyMode.prototype.eventMouseUp = function (event) {
    };

    EmptyMode.prototype.eventMouseOver = function (event) {
    };

    EmptyMode.prototype.eventMouseOut = function (event) {
    };

    EmptyMode.prototype.doAfter = function () {
    };

    EmptyMode.prototype.remove = function () {
    };

    EmptyMode.prototype.set = function (options) {
    };

    return EmptyMode;
}());
