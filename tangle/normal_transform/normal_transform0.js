//
//  ex08.js
//
//  A simple slider using Tangle (http://worrydream.com/Tangle/).
//  and TangleKitHYExt
//  (C) 2012 Hitoshi Yamauchi.  New BSD license.
//

(function () {

// MooTools: when DOM is ready, this is called
window.addEvent('domready', function () {

    // <div id="slider_example"> in ex08.html
    // This should contains all of this elements: canvas and point texts
    var container = document.getElementById("normal_transform_section");
    var tangle = new Tangle(container, {
        initialize: function () {
            this.px = 10;

            // point 0
            this.p0 = {}
            this.p0.x = -2;
            this.p0.y =  2;

            // point 1
            this.p1 = {}
            this.p1.x =  2;
            this.p1.y = -2;

            // matrix component (non homogeneous)
            //  [scale_x 0; 0 scale_y]
            this.scale_x = 1.0;
            this.scale_y = 1.0;
            //  [cos(th) -sin(th); sin(th) cos(th)]
            this.rotate_theta = 0.0;
            //  + [tx ty]'
            this.translate_x  = 0.0;
            this.translate_y  = 0.0;
        },
        update: function () {
            console.log("tangle updated")
        }
    });
    tangle.setValue("px", 40);
});

//----------------------------------------------------------
//  TKNormalTransformCanvas. control and view.
//    2D line and its normal visualization
Tangle.classes.TKNormalTransformCanvas = {

    initialize: function (element, options, tangle, px, py) {
        this.element = element;

        // view data object
        this.vdat.tangle     = tangle;
        this.vdat.canvas     = element;
        this.vdat.isDragging = false;

        // Hovering event
        // this.vdat.canvas.addEvent("mouseenter", function () {
        //     console.log("TKNormalTransformCanvas mouse enter event. " + tangle.getValue("px"));
        // });
        // this.vdat.canvas.addEvent("mouseleave", function () {
        //     console.log("TKNormalTransformCanvas mouse leave event. " + tangle.getValue("px"));
        // });

        // mouse down point
        this.vdat.pointer_start_x = 0;
        this.vdat.pointer_start_y = 0;

        var vdRef = this.vdat;

        // Dragging using BVTouchable
        new BVTouchable(element, {
            touchDidGoDown: function (touches) {
                vdRef.pointer_start_x = touches.event.client.x - vdRef.canvas.offsetParent.offsetLeft;
                vdRef.pointer_start_y = touches.event.client.y - vdRef.canvas.offsetParent.offsetTop;
                // console.log("BVTouchable: touchDidGoDown " + pointer_x + ", " + pointer_y)
                vdRef.isDragging = true;
                var obj = {}
                obj['px'] = vdRef.pointer_start_x;
                // obj['py'] = pointer_start_y;
                tangle.setValues(obj)
            },
            touchDidMove: function (touches) {
                var pointer_x = vdRef.pointer_start_x + touches.translation.x;
                var pointer_y = vdRef.pointer_start_y - touches.translation.y;
                // console.log("BVTouchable: touchDidMove "  + pointer_x + ", " + pointer_y)
                var obj = {}
                obj['px'] = pointer_x;
                // obj['py'] = pointer_y;
                vdRef.tangle.setValues(obj)
            },
            touchDidGoUp: function (touches) {
                // console.log("BVTouchable: touchDidGoUp")
                var pointer_x = vdRef.pointer_start_x + touches.translation.x;
                var pointer_y = vdRef.pointer_start_y - touches.translation.y;
                vdRef.isDragging = false;
                var obj = {}
                // tangle check the same value ... shift once and then adjust hack
                obj['px'] = pointer_x+1;
                vdRef.tangle.setValues(obj)
                obj['px'] = pointer_x;
                // obj['py'] = pointer_y;
                vdRef.tangle.setValues(obj)
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
        var canvasWidth  = mycanvas.width;
        var canvasHeight = mycanvas.height;
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
};                              // TKNormalTransformCanvas

})();
