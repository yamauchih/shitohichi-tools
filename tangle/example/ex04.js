//
//  ex04.js
//
//  Control/Draw a point using Tangle (http://worrydream.com/Tangle/).
//  (C) 2012 Hitoshi Yamauchi.  New BSD license.
//

function setUpTangle () {

    // <div id="point_position"> in ex4.html
    var element = document.getElementById("point_position");
    var points  = new Array();
    var mycanvas  = document.getElementById("canvas");
    var cxt       = mycanvas.getContext('2d');
    var maxHeight = mycanvas.height;

    var tangle = new Tangle(element, {
        initialize: function () {
            this.px = 30;
            this.py = 30;
        },
        update: function () {
            this.log("updated")
        }
    });

//----------------------------------------------------------
//
//  TKCanvasPoint
//  Drag a point.
//

    var isAnyAdjustableNumberDragging = false;  // hack for dragging one value over another one

Tangle.classes.TKCanvasPoint = {

    initialize: function (element, options, tangle, variable) {
        this.element = element;
        this.tangle  = tangle;
        this.variable = variable;

        // this.min = (options.min !== undefined) ? parseFloat(options.min) : 1;
        // this.max = (options.max !== undefined) ? parseFloat(options.max) : 10;
        // this.step = (options.step !== undefined) ? parseFloat(options.step) : 1;

        // this.initializeHover();
        // this.initializeHelp();
        // this.initializeDrag();
    },


    // hover
    // initializeHover: function () {
    //     this.isHovering = false;
    //     this.element.addEvent("mouseenter", (function () { this.isHovering = true;  this.updateRolloverEffects(); }).bind(this));
    //     this.element.addEvent("mouseleave", (function () { this.isHovering = false; this.updateRolloverEffects(); }).bind(this));
    // },

    updateRolloverEffects: function () {
        this.updateStyle();
        this.updateCursor();
        this.updateHelp();
    },

    isActive: function () {
        return this.isDragging || (this.isHovering && !isAnyAdjustableNumberDragging);
    },

    updateStyle: function () {
        if (this.isDragging) { this.element.addClass("TKAdjustableNumberDown"); }
        else { this.element.removeClass("TKAdjustableNumberDown"); }

        if (!this.isDragging && this.isActive()) { this.element.addClass("TKAdjustableNumberHover"); }
        else { this.element.removeClass("TKAdjustableNumberHover"); }
    },

    updateCursor: function () {
        var body = document.getElement("body");
        if (this.isActive()) { body.addClass("TKCursorDragHorizontal"); }
        else { body.removeClass("TKCursorDragHorizontal"); }
    },


    // help

    // initializeHelp: function () {
    //     this.helpElement = (new Element("div", { "class": "TKAdjustableNumberHelp" })).inject(this.element, "top");
    //     this.helpElement.setStyle("display", "none");
    //     this.helpElement.set("text", "drag");
    // },

    // updateHelp: function () {
    //     var size = this.element.getSize();
    //     var top = -size.y + 7;
    //     var left = Math.round(0.5 * (size.x - 20));
    //     var display = (this.isHovering && !isAnyAdjustableNumberDragging) ? "block" : "none";
    //     this.helpElement.setStyles({ left:left, top:top, display:display });
    // },


    // drag
    initializeDrag: function () {
        this.isDragging = false;
        new BVTouchable(this.element, this);
    },

    touchDidGoDown: function (touches) {
        this.valueAtMouseDown = this.tangle.getValue(this.variable);
        this.isDragging = true;
        isAnyAdjustableNumberDragging = true;
        this.updateRolloverEffects();
        this.updateStyle();
    },

    touchDidMove: function (touches) {
        var value = this.valueAtMouseDown + touches.translation.x / 5 * this.step;
        value = ((value / this.step).round() * this.step).limit(this.min, this.max);
        this.tangle.setValue(this.variable, value);
        this.updateHelp();
    },

    touchDidGoUp: function (touches) {
        this.helpElement.setStyle("display", "none");
        this.isDragging = false;
        isAnyAdjustableNumberDragging = false;
        this.updateRolloverEffects();
        this.updateStyle();
    }
};

};