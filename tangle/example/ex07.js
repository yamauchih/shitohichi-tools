//
//  ex07.js
//
//  A simple slider using Tangle (http://worrydream.com/Tangle/).
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
            this.px = 10;
            this.py = 15;
        },
        update: function () {
            console.log("tangle updated")
        }
    });
    tangle.setValue("px", 40);
});

//----------------------------------------------------------
//  Control: TKCanvasSlider
//    Mouse control tracker
//
//    Bret Victor's code is separating the model, view, and control in
//    the FilterExample.js (model: tangle, View: Filter*Plot, Control:
//    FilterKnob). I try to follow that idea here. However, this is my
//    first JavaScript and I am not able to do it yet.
//
//    I like Bret's jumping fancy slider, but, I have not enough
//    understanding of his code. This is simple version, but using his
//    images.
//

// This Tangle is a global variable defined in Tangle.js
Tangle.classes.TKCanvasSlider = {

    initialize: function (element, options, tangle, px, py) {
        this.element = element;
        this.tangle  = tangle;

        // all view related data are stored in this object
        this.vdat = {};

        // use function scope to refer in function literal
        // Or shall I extend BVTouchable initialize: function (el, delegate, option)
        // and pass this.vdat to BVTouchable?
        var vdRef = this.vdat;

        this.vdat.dataMin    = options.min ? parseFloat(options.min) :   0;
        this.vdat.dataMax    = options.max ? parseFloat(options.max) : 100;
        this.vdat.dataFormat = options.format ? options.format : "%.1f";
        if(this.vdat.dataMin >= this.vdat.dataMax){
            console.log("TKCanvasSlider illegal data-min, data-max value. [" +
                        this.vdat.dataMin + "," + this.vdat.dataMax + "], set to default.");
            this.vdat.dataMin = 0;
            this.vdat.dataMax = 100;
        }

        this.vdat.mycanvas = element.getParent().getElement("canvas");
        this.vdat.ctx      = this.vdat.mycanvas.getContext("2d");
        this.vdat.canvasWidth = this.vdat.mycanvas.width;

        // load knob image
        this.vdat.sliderYpos = 13;
        this.vdat.sliderKnobImg  = new Image();
        this.vdat.sliderLeftImg  = new Image();
        this.vdat.sliderRightImg = new Image();

        this.vdat.sliderKnobImg.onload = function(){
            vdRef.ctx.drawImage(vdRef.sliderKnobImg,
                                tangle.getValue("px"),
                                tangle.getValue("py") - (vdRef.sliderKnobImg.width / 2));
        }
        this.vdat.sliderLeftImg.onload = function(){
            vdRef.ctx.drawImage(vdRef.sliderLeftImg, 0, vdRef.sliderYpos);
        }
        this.vdat.sliderRightImg.onload = function(){
            vdRef.ctx.drawImage(vdRef.sliderRightImg,
                                vdRef.mycanvas.width - vdRef.sliderRightImg.width,
                                vdRef.sliderYpos);
        }
        this.vdat.sliderKnobImg.src  = 'Image/SliderKnob.png';
        this.vdat.sliderLeftImg.src  = 'Image/SliderLeft.png';
        this.vdat.sliderRightImg.src = 'Image/SliderRight.png';

        // Hovering event
        this.vdat.mycanvas.addEvent("mouseenter", function () {
            console.log("TKCanvasSlider mouse enter event. " + tangle.getValue("px"));
        });
        this.vdat.mycanvas.addEvent("mouseleave", function () {
            console.log("TKCanvasSlider mouse leave event. " + tangle.getValue("px"));
        });

        // mouse down point
        this.vdat.pointer_start_x = 0;
        this.vdat.pointer_x       = 0;
        this.vdat.pointer_y       = 15;
        this.vdat.isDragging      = false;

        // x position to value
        this.vdat.xToValue = function(x) {
            var dataSpan = this.dataMax - this.dataMin;
            return ((x / this.canvasWidth) * dataSpan) + this.dataMin;
        }
        // value to x position
        this.vdat.valueToX = function(v) {
            var dataSpan = this.dataMax - this.dataMin;
            return ((v - this.dataMin) / dataSpan) * this.canvasWidth;
        }

        // Dragging using BVTouchable
        new BVTouchable(element, {
            touchDidGoDown: function (touches) {
                vdRef.pointer_start_x =
                    touches.event.client.x - vdRef.mycanvas.offsetParent.offsetLeft;
                // console.log("BVTouchable: touchDidGoDown " + pointer_x)
                vdRef.isDragging = true;
                var obj = {}
                obj['px'] = vdRef.xToValue(vdRef.pointer_start_x);
                tangle.setValues(obj)
            },
            touchDidMove: function (touches) {
                vdRef.pointer_x = vdRef.pointer_start_x + touches.translation.x;
                // console.log("BVTouchable: touchDidMove "  + pointer_x)
                var obj = {}
                obj['px'] = vdRef.xToValue(vdRef.pointer_x);
                tangle.setValues(obj)
            },
            touchDidGoUp: function (touches) {
                // console.log("BVTouchable: touchDidGoUp")
                vdRef.pointer_x = vdRef.pointer_start_x + touches.translation.x;
                vdRef.isDragging = false;
                var obj = {}
                // tangle check the same value ... shift once and then adjust, a hack
                obj['px'] = vdRef.xToValue(vdRef.pointer_x) + 1;
                tangle.setValues(obj)
                obj['px'] = vdRef.xToValue(vdRef.pointer_x);
                tangle.setValues(obj)
            }
        });                     // new BVTouchable
    },                          // initialize function

    update: function (el, px) {
        console.log("update: " + px);
        this.drawCanvas(el, px);
    },                      // update function

    drawCanvas: function(el, px) {
        // assmed element is a canvas
        var mycanvas     = el;
        var canvasHeight = mycanvas.height;
        var ctx          = mycanvas.getContext("2d");

        ctx.fillStyle = "#ffffff";
        ctx.fillRect(0, 0, this.vdat.canvasWidth, canvasHeight);

        var point = {}
        if(this.vdat.isDragging){
            point.x = this.vdat.pointer_x;
        }
        else{
            point.x = this.vdat.valueToX(px);
        }
        point.y   = this.vdat.pointer_y;

        var lineOffset = 8;     // == sliderLeft.width == sliderRight.width

        // draw background 116(74), 181(b5), 215(d7), 215(d7)
        var colary = ['#747474', '#b5b5b5', '#d7d7d7', '#d7d7d7'];
        ctx.lineWidth = 1;
        for(var i = 0; i < colary.length; ++i){
            ctx.beginPath();
            ctx.strokeStyle = colary[i];
            ctx.moveTo(lineOffset, this.vdat.sliderYpos + i + 1);
            ctx.lineTo(this.vdat.canvasWidth - lineOffset, this.vdat.sliderYpos + i + 1);
            ctx.stroke();
            ctx.closePath();
        }
        ctx.drawImage(this.vdat.sliderLeftImg,  0, this.vdat.sliderYpos);
        ctx.drawImage(this.vdat.sliderRightImg,
                      this.vdat.canvasWidth - this.vdat.sliderRightImg.width,
                      this.vdat.sliderYpos);

        this.drawPoint(ctx, point);
    },

    drawPoint: function(ctx, point) {
        var knobRadius = this.vdat.sliderKnobImg.width / 2;

        ctx.drawImage(this.vdat.sliderKnobImg, point.x - knobRadius, point.y - knobRadius);
        if(this.vdat.isDragging){
            ctx.fillStyle = "#444444";
            var valtext = sprintf(this.vdat.dataFormat, this.vdat.xToValue(point.x));
            ctx.fillText('[' + valtext + ']',
                         point.x, point.y - knobRadius - 2);
        }
    }
};                              // TKCanvasSlider

})();
