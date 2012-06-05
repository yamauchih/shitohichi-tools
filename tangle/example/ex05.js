//
//  ex05.js
//
//  Control/Draw a point using Tangle (http://worrydream.com/Tangle/).
//  (C) 2012 Hitoshi Yamauchi.  New BSD license.
//

//
//  Element structure
//    point_drag_example
//      + point_drag_canvas
//      + point_dynamic_text
//

(function () {

// MooTools: when DOM is ready, this is called
window.addEvent('domready', function () {

    // <div id="point_drag_example"> in ex4.html
    // This should contains all of this elements: canvas and point texts
    var container = document.getElementById("point_drag_example");
    var tangle = new Tangle(container, {
        initialize: function () {
            this.px = 30;
            this.py = 30;
        },
        update: function () {
            console.log("tangle updated")
        }
    });
    tangle.setValue("px", 40);
});

//----------------------------------------------------------
//  Control: TKCanvasControl
//    Mouse control tracker
//
//    Bret Victor's code is separating the model, view, and control in
//    the FilterExample.js (model: tangle, View: Filter*Plot, Control:
//    FilterKnob). I try to follow that idea here.
//

// I don't know how to pass this control state.
// via Tangle with data-var sounds wrong since these should be a model.
var isDragging = false;

// This Tangle is a global variable defined in Tangle.js
Tangle.classes.TKCanvasControl = {

    initialize: function (element, options, tangle, px, py) {
        this.element = element;
        this.tangle  = tangle;

        // point_drag_example
        var mycanvas     = element.getParent().getElement("canvas");

        // Hovering event
        mycanvas.addEvent("mouseenter", function () {
            console.log("TKCanvasControl mouse enter event. " + tangle.getValue("px"));
        });
        mycanvas.addEvent("mouseleave", function () {
            console.log("TKCanvasControl mouse leave event. " + tangle.getValue("px"));
        });

        // mouse down point
        var pointer_start_x = 0;
        var pointer_start_y = 0;

        // Dragging using BVTouchable
        new BVTouchable(element, {
            touchDidGoDown: function (touches) {
                pointer_start_x = touches.event.client.x - mycanvas.offsetParent.offsetLeft;
                pointer_start_y = touches.event.client.y - mycanvas.offsetParent.offsetTop;
                // console.log("BVTouchable: touchDidGoDown " + pointer_x + ", " + pointer_y)
                isDragging = true;
                var obj = {}
                obj['px'] = pointer_start_x;
                obj['py'] = pointer_start_y;
                obj['isDragging'] = pointer_start_y;
                tangle.setValues(obj)
            },
            touchDidMove: function (touches) {
                pointer_x = pointer_start_x + touches.translation.x;
                pointer_y = pointer_start_y - touches.translation.y;
                // console.log("BVTouchable: touchDidMove "  + pointer_x + ", " + pointer_y)
                var obj = {}
                obj['px'] = pointer_x;
                obj['py'] = pointer_y;
                tangle.setValues(obj)
            },
            touchDidGoUp: function (touches) {
                // console.log("BVTouchable: touchDidGoUp")
                pointer_x = pointer_start_x + touches.translation.x;
                pointer_y = pointer_start_y - touches.translation.y;
                isDragging = false;
                var obj = {}
                // tangle check the same value ... shift once and then adjust hack
                obj['px'] = pointer_x+1;
                tangle.setValues(obj)
                obj['px'] = pointer_x;
                obj['py'] = pointer_y;
                tangle.setValues(obj)
            }
        });                     // new BVTouchable
    },                          // initialize function

    update: function (el, px, py) {
        // console.log("update: " + px + ", " + py);
        this.drawCanvas(el, px, py);
    },                      // update function

    drawCanvas: function(el, px, py) {
        // assmed element is a canvas
        var mycanvas     = el;
        var canvasWidth  = mycanvas.get("width");
        var canvasHeight = mycanvas.get("height");
        var ctx          = mycanvas.getContext("2d");

        ctx.fillStyle = "#fff";
        ctx.fillRect(0, 0, canvasWidth, canvasHeight);

        var point = {}
        point.x     = px;
        point.y     = py;
        point.label = "0";
        this.drawPoint(ctx, point);
    },

    drawPoint: function(ctx, point) {
        pointRadius = 6;
        ctx.fillStyle = "#ff0000";
        ctx.beginPath();
        ctx.arc(point.x, point.y, pointRadius, 0, Math.PI*2, true);
        ctx.closePath();
        ctx.fill();
        ctx.fillStyle = "#FFFFFF";
        ctx.fillText(point.label, point.x - 3, point.y + 4);
        if(isDragging){
            ctx.fillStyle = "#444444";
            ctx.fillText('[' + point.x + ':' + point.y + ']',
                         point.x + pointRadius + 2, point.y + pointRadius + 2);
        }
    }
};                              // TKCanvasControl

})();
