//
// based on bezier example.
//

// import image: If you do this, don't do <body onload="setUpTangle();"> in html file
//var pointImage = new Image();
//pointImage.onload = setUpTangle;
//pointImage.src = "point.png";

function setUpTangle () {

    var element   = document.getElementById("point");
    var points    = new Array();
    var theCanvas = document.getElementById("canvas");
    var context   = theCanvas.getContext('2d');
    var maxHeight = theCanvas.height;
    var maxWidth  = theCanvas.width;
    var mouseDrag = false;
    var mouseOver = new Array();
    var cpRadius = 6;           // how close to the point

    var tangle = new Tangle(element, {
        initialize: function () {
            this.p0x = 30;
            this.p0y = 30;
            this.refresh = 0;
        },
        update: function () {
            drawCanvas(this);
        }
    });

    function drawCanvas(tangleObj) {
        context.fillStyle = "#EEEEEE";
        context.fillRect(0, 0, maxWidth, maxHeight);
        // draw the control points
        drawPoint({x:tangleObj.p0x, y:tangleObj.p0y, label:0});
        // console.log("drawCanvas")
    }

    function drawPoint(point) {
        hover = mouseOver[point.label];
        context.fillStyle = "#ff0000";
        // console.log('hover: ' + hover);
        if(hover){
            context.fillStyle = "#009999";
        }

        context.beginPath();
        context.arc(point.x, point.y, cpRadius, 0, Math.PI*2, true);
        context.closePath();
        context.fill();
        context.fillStyle = "#FFFFFF";
        context.fillText(point.label, point.x-3, point.y+4);
        if(hover){
            context.fillStyle = "#444444";
            context.fillText('[' + point.x + ':' + point.y + ']', point.x+8, point.y+8);
        }
    }

    function onMouseMove(e) {
        mouseX = e.clientX - theCanvas.offsetLeft;
        if(mouseX > maxWidth){
            mouseX = maxWidth;
        }
        mouseY = e.clientY - theCanvas.offsetTop;
        if(mouseY > maxHeight){
            mouseY = maxHeight;
        }
        // console.log('Mouse: ' + mouseX + ' x ' + mouseY + " / " + e.clientX + ' x ' + e.clientY);
        if(mouseDrag){
            // console.log('starting drag on ' + mouseTarget);
            // what am I dragging?
            switch(mouseTarget){
            case '0':
                tangle.setValue('p0x', mouseX);
                tangle.setValue('p0y', mouseY);
                break;
            }
        }else{
            mouseOverCheck({x:tangle.getValue('p0x'),y:tangle.getValue('p0y'),label:'0'});
            // console.log("no dragging " + mouseOver);
        }
        // hack for getting tangle to call update
        tangle.setValue('refresh', Math.random());
    }

    function mouseOverCheck(target){
        //console.dir(target);
        mouseOver[target.label] = false;
        var dx = target.x - mouseX;
        var dy = target.y - mouseY;
        var distance = (dx * dx + dy * dy);
        //console.log('distance: ' + distance);
        if (distance <= (cpRadius) * (cpRadius)){
            // console.log('mouse over ' + target.label);
            mouseOver[target.label] = target.label;
            return true;
        }else{
            return false;
        }
    }

    function eventMouseDown(event) {
        // console.log('mouse down ' + mouseOver);
        for(var i = 0; i < mouseOver.length; i++){
            //console.log('Testing '+ i + ': ' +mouseOver[i])
            if(mouseOver[i]!== false){
                mouseDrag = true;
                mouseTarget = mouseOver[i];
                //console.log('mouse down: ' + mouseTarget);
            }
        }
    }

    function eventMouseUp(event) {
        // console.log('mouse up')
        mouseDrag = false;
        mouseTarget = null;
    }

    theCanvas.addEventListener("mousemove", onMouseMove,    false);
    theCanvas.addEventListener("mouseup",   eventMouseUp,   false);
    theCanvas.addEventListener("mousedown", eventMouseDown, false);
}