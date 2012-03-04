// import image
var pointImage = new Image();
pointImage.onload = setUpTangle;
pointImage.src = "point.png";

function setUpTangle () {

    var element = document.getElementById("formulas");
    var points = new Array();
    // bezier coeffcients
    var cx;
    var bx;
    var ax;
    var cy;
    var by;
    var ay;

    var ball = {x:0, y:0, speed:0.01, t:.5};

    var mouseX;
    var mouseY;
    var mouseDrag = false;
    var mouseTarget;
    var mouseOver = new Array;

    var cpRadius = 6;

    //    if(Modernizr.canvas){
    var theCanvas = document.getElementById("canvas");
    var context = theCanvas.getContext('2d');
    var maxHeight = theCanvas.height - 30;
    //    }

    var tangle = new Tangle(element, {
        initialize: function () {
            this.p0x = 30;
            this.p0y = 470;
            this.p1x = 30;
            this.p1y = 30;

            this.p2x = 430;
            this.p2y = 30;
            this.p3x = 430;
            this.p3y = 470;
            this.t = .50;
            this.refresh = 0;
            this.cx = cx;
            this.bx = bx;
            this.ax = ax;
            this.cy = cy;
            this.by = by;
            this.ay = ay;
            this.xt = this.p0x;
            this.yt = this.p0y;
        },
        update: function () {
            ball.t = this.t;
            calculatePoints(this);
            drawCanvas(this);
            this.cx = cx;
            this.bx = bx;
            this.ax = ax;
            this.cy = cy;
            this.by = by;
            this.ay = ay;
            this.tSqr = this.t * this.t;
            this.tCube = this.t * this.t * this.t;
        }
    });

    function drawCanvas(tangleObj) {

        context.fillStyle = "#EEEEEE";
        context.fillRect(0, 0, theCanvas.width, maxHeight);

        drawPoints();

        // draw handles
        context.strokeStyle = "#00FF00";
        context.lineWidth = 1;
        context.beginPath();
        context.moveTo(tangleObj.p0x, tangleObj.p0y);
        context.lineTo(tangleObj.p1x, tangleObj.p1y);
        context.stroke();
        context.closePath();
        context.beginPath();
        context.moveTo(tangleObj.p2x, tangleObj.p2y);
        context.lineTo(tangleObj.p3x, tangleObj.p3y);
        context.stroke();
        context.closePath();

        // drwaw the control points
        controlPoint({x:tangleObj.p0x,y:tangleObj.p0y,label:'0'});
        controlPoint({x:tangleObj.p1x,y:tangleObj.p1y,label:'1'});
        controlPoint({x:tangleObj.p2x,y:tangleObj.p2y,label:'2'});
        controlPoint({x:tangleObj.p3x,y:tangleObj.p3y,label:'3'});

        drawBall(tangleObj);


    }

    function calculatePoints(tangleObj){
        points = new Array();
        cx = 3* (tangleObj.p1x -tangleObj.p0x);
        bx = 3 * (tangleObj.p2x -tangleObj.p1x) -cx;
        ax = tangleObj.p3x - tangleObj.p0x - cx - bx;

        cy = 3* (tangleObj.p1y -tangleObj.p0y);
        by = 3 * (tangleObj.p2y -tangleObj.p1y) -cy;
        ay = tangleObj.p3y - tangleObj.p0y - cy - by;

        for(var t=0; t <= 1; t+=.01){
            var xt = ax*(t*t*t) + bx*(t*t) + cx*t + tangleObj.p0x;
            var yt = ay*(t*t*t) + by*(t*t) + cy*t + tangleObj.p0y;
            points.push({x:xt, y:yt});
        }
    }

    function drawPoints() {
        for (var i = 0; i < points.length; i++) {
            context.drawImage(pointImage, points[i].x, points[i].y, 1, 1);
        }
    }

    function controlPoint(point) {
        hover = mouseOver[point.label];
        context.fillStyle = "#ff0000";
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

    function drawBall(tangleObj) {
        var t = ball.t;
        var xt = ax*(t*t*t) + bx*(t*t) + cx*t + tangleObj.p0x;
        var yt = ay*(t*t*t) + by*(t*t) + cy*t + tangleObj.p0y;
        tangleObj.xt = xt;
        tangleObj.yt = yt;

        context.fillStyle = "#000000";
        context.beginPath();
        context.arc(xt, yt, 5, 0, Math.PI*2, true);
        context.closePath();
        context.fill();

        // draw x & y lines
        context.strokeStyle = "#ccc";
        context.lineWidth = 1;
        context.beginPath();
        context.moveTo(xt,0);
        context.lineTo(xt, maxHeight);
        context.stroke();
        context.closePath();

        context.beginPath();
        context.moveTo(0, yt);
        context.lineTo(theCanvas.width, yt);
        context.stroke();
        context.closePath();
    }

    function onMouseMove(e) {
        mouseX = e.clientX - theCanvas.offsetLeft;
        if(mouseX>490){
            mouseX = 490;
        }
        mouseY = e.clientY - theCanvas.offsetTop;
        if(mouseY>490){
            mouseY = 490;
        }
        //console.log('Mouse: ' + mouseX + ' x ' + mouseY + " / " + e.clientX + ' x ' + e.clientY);
        if(mouseDrag){
            //console.log('starting drag on ' + mouseTarget);
            // what am I dragging?
            switch(mouseTarget){
                case  '0':
                    tangle.setValue('p0x', mouseX);
                    tangle.setValue('p0y', mouseY);
                    break;
                case  '1':
                    tangle.setValue('p1x', mouseX);
                    tangle.setValue('p1y', mouseY);
                    break;
                case  '2':
                    tangle.setValue('p2x', mouseX);
                    tangle.setValue('p2y', mouseY);
                    break;
                case  '3':
                    tangle.setValue('p3x', mouseX);
                    tangle.setValue('p3y', mouseY);
                    break;

            }
            calculatePoints(tangle);
        }else{
            mouseOverCheck({x:tangle.getValue('p0x'),y:tangle.getValue('p0y'),label:'0'});
            mouseOverCheck({x:tangle.getValue('p1x'),y:tangle.getValue('p1y'),label:'1'});
            mouseOverCheck({x:tangle.getValue('p2x'),y:tangle.getValue('p2y'),label:'2'});
            mouseOverCheck({x:tangle.getValue('p3x'),y:tangle.getValue('p3y'),label:'3'});
            //console.log(mouseOver);
        }
        // hack for getting tangle to call update
        tangle.setValue('refresh',Math.random());
    }

    function mouseOverCheck(target){
        //console.dir(target);
        mouseOver[target.label] = false;
        var dx = target.x - mouseX;
        var dy = target.y - mouseY;
        var distance = (dx * dx + dy * dy);
        //console.log('distance: ' + distance);
        if (distance <= (cpRadius) * (cpRadius)){
            //console.log('mouse over ' + target.label);
            mouseOver[target.label] = target.label;
            return true;
        }else{
            return false;
        }
    }

    function eventMouseDown(event) {
        //console.log('mouse down');
        //console.log(mouseOver);
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
        mouseDrag = false;
        mouseTarget = null;
    }

    theCanvas.addEventListener("mousemove", onMouseMove, false);
    theCanvas.addEventListener("mouseup", eventMouseUp, false);
    theCanvas.addEventListener("mousedown", eventMouseDown, false);
}