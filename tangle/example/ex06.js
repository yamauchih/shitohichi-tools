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
//    I love Bret's jumping fancy slider, but, I have not enough
//    understanding of his code. This is simple version, but using his
//    images.
//

// I don't know how to pass this control state.
// via Tangle with data-var sounds wrong since these should be a model.
// Using global seems not well.
var isDragging = false;
var knobRadius = 6;

// This Tangle is a global variable defined in Tangle.js
Tangle.classes.TKCanvasSlider = {

    initialize: function (element, options, tangle, px, py) {
        this.element = element;
        this.tangle  = tangle;
        this.dataMin = options.min ? parseFloat(options.min) :   0;
        this.dataMax = options.max ? parseFloat(options.max) : 100;
        if(this.dataMin >= this.dataMax){
            console.log("TKCanvasSlider illegal data-min, data-max value. [" +
                        this.dataMin + "," + this.dataMax + "], set to default.");
            this.dataMin = 0;
            this.dataMax = 100;
        }

        // point_drag_example
        var mycanvas     = element.getParent().getElement("canvas");
        var ctx          = mycanvas.getContext("2d");
        this.canvasWidth = mycanvas.width;

        // load knob image
        this.sliderYpos = 13;
        var ypos = this.sliderYpos; // This looks also strange "this" and "var".
        this.sliderKnobImg  = new Image();
        this.sliderLeftImg  = new Image();
        this.sliderRightImg = new Image();
        // can not use this.sliderKnobImg in the following function.
        var knobimg  = this.sliderKnobImg;
        var leftimg  = this.sliderLeftImg;
        var rightimg = this.sliderRightImg;
        this.sliderKnobImg.onload = function(){
            ctx.drawImage(knobimg, tangle.getValue("px"), tangle.getValue("py") - knobRadius);
        }
        this.sliderLeftImg.onload = function(){
            ctx.drawImage(leftimg, 0, ypos);
        }
        this.sliderRightImg.onload = function(){
            ctx.drawImage(rightimg, mycanvas.width - rightimg.width, ypos);
        }
        this.sliderKnobImg.src  = 'Image/SliderKnob.png';
        this.sliderLeftImg.src  = 'Image/SliderLeft.png';
        this.sliderRightImg.src = 'Image/SliderRight.png';

        // Hovering event
        mycanvas.addEvent("mouseenter", function () {
            console.log("TKCanvasSlider mouse enter event. " + tangle.getValue("px"));
        });
        mycanvas.addEvent("mouseleave", function () {
            console.log("TKCanvasSlider mouse leave event. " + tangle.getValue("px"));
        });

        // mouse down point
        var pointer_start_x = 0;
        var pointer_start_y = 0;

        // Dragging using BVTouchable
        new BVTouchable(element, {
            touchDidGoDown: function (touches) {
                pointer_start_x = touches.event.client.x - mycanvas.offsetParent.offsetLeft;
                // console.log("BVTouchable: touchDidGoDown " + pointer_x + ", " + pointer_y)
                isDragging = true;
                var obj = {}
                obj['px'] = pointer_start_x; // TODO: extend tangle to get x <-> value
                obj['isDragging'] = pointer_start_y;
                tangle.setValues(obj)
            },
            touchDidMove: function (touches) {
                pointer_x = pointer_start_x + touches.translation.x;
                // console.log("BVTouchable: touchDidMove "  + pointer_x + ", " + pointer_y)
                var obj = {}
                obj['px'] = pointer_x;
                tangle.setValues(obj)
            },
            touchDidGoUp: function (touches) {
                // console.log("BVTouchable: touchDidGoUp")
                pointer_x = pointer_start_x + touches.translation.x;
                isDragging = false;
                var obj = {}
                // tangle check the same value ... shift once and then adjust hack
                obj['px'] = pointer_x+1;
                tangle.setValues(obj)
                obj['px'] = pointer_x;
                tangle.setValues(obj)
            }
        });                     // new BVTouchable
    },                          // initialize function

    update: function (el, px, py) {
        console.log("update: " + px + ", " + py);
        this.drawCanvas(el, px, py);
    },                      // update function

    drawCanvas: function(el, px, py) {
        // assmed element is a canvas
        var mycanvas     = el;
        var canvasHeight = mycanvas.height;
        var ctx          = mycanvas.getContext("2d");

        ctx.fillStyle = "#ffffff";
        // ctx.fillStyle = "#000";
        ctx.fillRect(0, 0, this.canvasWidth, canvasHeight);

        var point = {}
        point.x   = px;
        point.y   = py;

        var lineOffset = 8;     // == sliderLeft.width == sliderRight.width

        // draw background 116(74), 181(b5), 215(d7), 215(d7)
        var colary = ['#747474', '#b5b5b5', '#d7d7d7', '#d7d7d7'];
        ctx.lineWidth = 1;
        for(var i = 0; i < colary.length; ++i){
            ctx.beginPath();
            ctx.strokeStyle = colary[i];
            ctx.moveTo(lineOffset,                    this.sliderYpos + i + 1);
            ctx.lineTo(this.canvasWidth - lineOffset, this.sliderYpos + i + 1);
            ctx.stroke();
            ctx.closePath();
        }
        ctx.drawImage(this.sliderLeftImg,  0, this.sliderYpos);
        ctx.drawImage(this.sliderRightImg, this.canvasWidth - this.sliderRightImg.width,
                      this.sliderYpos);

        this.drawPoint(ctx, point);
    },

    drawPoint: function(ctx, point) {
        // var dataLen = this.dataMax - this.dataMin;
        // var knobX = ((point.x - this.dataMin) / dataLen) * canvasWidth;

        ctx.drawImage(this.sliderKnobImg, point.x, point.y - knobRadius);
        if(isDragging){
            ctx.fillStyle = "#444444";
            ctx.fillText('[' + this.xToValue(point.x) + ']',
                         point.x, point.y - knobRadius - 2);
        }
    }
    ,

    /// get the value from mouse x coordinates
    xToValue: function(x) {
        var dataSpan = this.dataMax - this.dataMin;
        return ((x / this.canvasWidth) * dataSpan) + this.dataMin;
    },

    /// get mouse x coordinates from the value
    valueToX: function(v) {
        var dataSpan = this.dataMax - this.dataMin;
        return ((v - this.dataMin) / dataSpan) * this.canvasWidth;
    }


};                              // TKCanvasSlider

})();
