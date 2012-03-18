//
//  normal_transform0.js
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

            // point 0 (homogenious coordinates)
            this.p0 = new hyVector3([-2,  2, 1]);
            // point 1
            this.p1 = new hyVector3([ 2, -2, 1]);

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
        this.vdat = {};
        this.vdat.tangle     = tangle;
        this.vdat.canvas     = element;
        this.vdat.ctx        = this.vdat.canvas.getContext("2d");
        this.vdat.isDragging = false;

        // Hovering event
        // this.vdat.canvas.addEvent("mouseenter", function () {
        //     console.log("TKNormalTransformCanvas mouse enter event. " + tangle.getValue("px"));
        // });
        // this.vdat.canvas.addEvent("mouseleave", function () {
        //     console.log("TKNormalTransformCanvas mouse leave event. " + tangle.getValue("px"));
        // });

        var sx = this.vdat.canvas.width  / 8.0;
        var sy = this.vdat.canvas.height / 8.0;
        var scalemat = new hyMatrix33();
        scalemat.setEye();
        scalemat.setScale2D(sx, sy);
        console.log("scalemat: " + scalemat);

        var tx = this.vdat.canvas.width  / 2.0;
        var ty = this.vdat.canvas.height / 2.0;
        var transmat = new hyMatrix33();
        transmat.setEye();
        transmat.setTranslation2D(tx, ty);
        console.log("transformmat: " + transmat);

        this.vdat.modelToViewMat = new hyMatrix33();
        this.vdat.modelToViewMat.multiply(transmat, scalemat, this.vdat.modelToViewMat);
        console.log("modelToViewMat: " + this.vdat.modelToViewMat);
        // var p0 = this.vdat.tangle.getValue("p0");
        // var p1 = this.vdat.tangle.getValue("p1");
        var p0 = new hyVector3([-2,  2, 1]);
        var p1 = new hyVector3([ 2, -2, 1]);
        this.vdat.p0v3 = p0.clone();
        this.vdat.p1v3 = p1.clone();

        // mouse down point
        this.vdat.pointer_start_x = 0;
        this.vdat.pointer_start_y = 0;

        var vdRef = this.vdat;

        // background image
        this.vdat.coordinateBg = new Image();
        this.vdat.coordinateBg.onload = function(){
            vdRef.ctx.drawImage(vdRef.coordinateBg, 0, 0);
        }
        this.vdat.coordinateBg.src  = 'Image/coordinate_system.png';


        // Setup dragging using BVTouchable
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
        this.drawCanvas(el);
    },                      // update function

    drawCanvas: function(el) {
        // assmed element is a canvas
        var mycanvas     = el;
        var canvasWidth  = mycanvas.width;
        var canvasHeight = mycanvas.height;
        var ctx          = mycanvas.getContext("2d");

        ctx.fillStyle = "#fff";
        ctx.fillRect(0, 0, canvasWidth, canvasHeight);
        ctx.drawImage(this.vdat.coordinateBg,  0, 0);

        var p0 = this.vdat.tangle.getValue("p0");
        var p1 = this.vdat.tangle.getValue("p1");


        // model to view.
        //   The canvas center is (0,0).
        //   The canvas size is [-4,4]x[-4,4].
        this.vdat.p0v3 = this.vdat.modelToViewMat.transformPoint(p0);
        this.vdat.p1v3 = this.vdat.modelToViewMat.transformPoint(p1);

        console.log("update: " + this.vdat.p0v3 + "\n" + this.vdat.p1v3);

        this.drawPlane(ctx, this.vdat.p0v3, this.vdat.p1v3);
    },

    drawPlane: function(ctx, p0, p1) {
        var xoffset = 1;
        var yoffset = 1;

        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.strokeStyle = '#0f0f0f';
        ctx.moveTo(p0.m_element[0] + xoffset, p0.m_element[1] + yoffset);
        ctx.lineTo(p1.m_element[0] + xoffset, p1.m_element[1] + yoffset);
        ctx.stroke();
        ctx.closePath();

    }
};                              // TKNormalTransformCanvas

})();
