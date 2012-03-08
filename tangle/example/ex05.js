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
//  TKCanvasPoint
//  Drag a point.

// This Tangle is a global variable defined in Tangle.js
Tangle.classes.TKCanvasPoint = {

    initialize: function (element, options, tangle, px, py) {
        this.element = element;
        this.tangle  = tangle;
        this.px = 0;
        this.py = 0;

        // point_drag_example
        var mycanvas     = element.getParent().getElement("canvas");
        var cxt          = mycanvas.getContext("2d");
        var canvasWidth  = mycanvas.width;
        var canvasHeight = mycanvas.height;
        console.log("canvas w: " + canvasWidth + ", h: " + canvasHeight);

        // update
        this.update = function(el, px, py) {
            console.log("TKCanvasPoint updated: ");
        }

        // Hovering event
        mycanvas.addEvent("mouseenter", function () {
            console.log("TKCanvasPoint mouse enter event. " + tangle.getValue("px"));
        });
        mycanvas.addEvent("mouseleave", function () {
            console.log("TKCanvasPoint mouse leave event. " + tangle.getValue("px"));
        });

        // Dragging via BVTouchable
        new BVTouchable(this.element, {
            touchDidGoDown: function (touches) {
                console.log("BVTouchable: touchDidGoDown")
                tangle.setValue("px", Math.random())
            },
            touchDidMove: function (touches) {
                console.log("BVTouchable: touchDidMove")
                tangle.setValue("px", Math.random())
            },
            touchDidGoUp: function (touches) {
                console.log("BVTouchable: touchDidGoUp")
                tangle.setValue("px", Math.random())
            }
        });                     // new BVTouchable
    }                           // initialize function
};                              // TKCanvasPoint

})();
