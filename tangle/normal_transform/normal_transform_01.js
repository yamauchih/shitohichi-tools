///
/// normal_transform_01.js
///
///  A simple slider using Tangle (http://worrydream.com/Tangle/).
///  and TangleKitHYExt
///  (C) 2012 Hitoshi Yamauchi.  New BSD license.
///
/// \file
/// \brief normal transformation explanation tangle

(function () {
/// MooTools: when DOM is ready, this is called
window.addEvent('domready', function () {

    /// <div id="slider_example"> in ex08.html
    /// This should contains all of this elements: canvas and point texts
    var container = document.getElementById("normal_transform_section");
    var tangle = new Tangle(container, {
        /// initialize tangle
        initialize: function () {

            this.px = 0;   //FIXME: the slide depends on this variable

            // point 0 and 1's interface. We need to update this.p0 according to this value.
            this.p0x = 0;
            this.p0y = 0;
            this.p1x = 2;
            this.p1y = 2;

            // points 0 (homogenious coordinates)
            this.p0 = new hyVector3([ this.p0x, this.p0y, 1]);
            this.p1 = new hyVector3([ this.p1x, this.p1y, 1]);

            // normal: origin and direction (homogenious coordinates)
            this.normalOrigin = new hyVector3();
            this.normalDir    = new hyVector3();
            this.computeNormal(this.p0, this.p1, this.normalOrigin, this.normalDir);

            // matrix component (non homogeneous)
            //  [scale_x 0; 0 scale_y]
            this.scale_x = 1.0;
            this.scale_y = 1.0;
            //  [cos(th) -sin(th); sin(th) cos(th)]
            this.rotate_theta_deg = 0.0;
            this.rotate_theta_rad = 0.0;
            //  + [tx ty]'
            this.translation_x  = 0.0;
            this.translation_y  = 0.0;

            //----------------------------------------------------------------------
            // manipuration matrix
            this.scaleMat  = new hyMatrix33();
            this.rotateMat = new hyMatrix33();
            this.transMat  = new hyMatrix33();
            this.scaleMat. setEye();
            this.rotateMat.setEye();
            this.transMat. setEye();
            this.scaleMat. setScale2D(this.scale_x, this.scale_y);
            this.rotateMat.setRotation2D(this.rotate_theta_deg);
            this.transMat. setTranslation2D(this.translation_x, this.translation_y);

            this.manipMat = new hyMatrix33();
            this.tmpMat   = new hyMatrix33();
            this.manipMat.setEye();
            this.tmpMat.  setEye();

            // matrix positioning
            var smatpos = { bx:12, by:4, sx:35, sy:24, w:30, h:22 };
            this.setupMatrixElement("scale", smatpos);

            // set up rotate matrix position
            var rmatpos = { bx:48, by:4, sx:95, sy:24, w:30, h:22, offset12:10 };
            this.setupMatrixElement("rotate", rmatpos);

            // set up point1 vector position
            var pvecpos = { bx:10, by:4, sx:95, sy:24, w:30, h:22 };
            this.setupColumnVectorElement("p1", pvecpos);

            // set up transformation vector position
            var tvecpos = { bx:10, by:4, sx:95, sy:24, w:30, h:22 };
            this.setupColumnVectorElement("translation", tvecpos);
        },

        /// tangle update
        update: function () {
            // console.log("tangle updated")
            this.p0.set(0, this.p0x);
            this.p0.set(1, this.p0y);
            this.p1.set(0, this.p1x);
            this.p1.set(1, this.p1y);
            this.computeNormal(this.p0, this.p1, this.normalOrigin, this.normalDir);

            this.scaleMat. setScale2D(this.scale_x, this.scale_y);
            this.rotate_theta_rad = this.rotate_theta_deg * Math.PI / 180.0;
            // minus here. display coordinate issue.
            this.rotateMat.setRotation2D(-this.rotate_theta_rad);
            this.transMat. setTranslation2D(this.translation_x, this.translation_y);

            hyMatrix33.multiply(this.scaleMat, this.rotateMat, this.tmpMat);
            hyMatrix33.multiply(this.tmpMat,   this.transMat,  this.manipMat);
            // console.log("manipmat:\n" + this.manipMat);
        },

        /// matrix coefficient setup (positioning of the element)
        setupMatrixElement: function (matname, matpos) {
            // set up scale matrix position
            var mat_11_el = document.getElementById(matname + "_11_id");
            var mat_12_el = document.getElementById(matname + "_12_id");
            var mat_21_el = document.getElementById(matname + "_21_id");
            var mat_22_el = document.getElementById(matname + "_22_id");
            var bx = matpos.bx; // base x
            var by = matpos.by; // base y
            var sx = matpos.sx; // span x
            var sy = matpos.sy; // span y
            var w  = matpos.w;  // width
            var h  = matpos.h;  // height
            var pos11 = "left:" +  bx +       "px; top:" + by        + "px; width:" + w + "px; height:22px";
            var pos12;
            if(matpos["offset12"] != null){
                pos12 = "left:" + (bx + sx + matpos.offset12) + "px; top:" + by
                    + "px; width:" + w + "px; height:22px";
            }
            else{
                pos12 = "left:" + (bx + sx) + "px; top:" + by + "px; width:" + w + "px; height:22px";
            }
            var pos21 = "left:" +  bx +       "px; top:" + (by + sy) + "px; width:" + w + "px; height:22px";
            var pos22 = "left:" + (bx + sx) + "px; top:" + (by + sy) + "px; width:" + w + "px; height:22px";
            mat_11_el.style.cssText = pos11;
            mat_12_el.style.cssText = pos12;
            mat_21_el.style.cssText = pos21;
            mat_22_el.style.cssText = pos22;
        },

        /// column vector setup (positioning of the element)
        setupColumnVectorElement: function (vecname, vecpos) {
            // set up scale matrix position
            var vec_11_el = document.getElementById(vecname + "_11_id");
            var vec_21_el = document.getElementById(vecname + "_21_id");
            var bx = vecpos.bx; // base x
            var by = vecpos.by; // base y
            var sx = vecpos.sx; // span x: not used
            var sy = vecpos.sy; // span y
            var w  = vecpos.w;  // width
            var h  = vecpos.h;  // height
            var pos11 = "left:" +  bx +       "px; top:" + by        + "px; width:" + w + "px; height:22px";
            var pos21 = "left:" +  bx +       "px; top:" + (by + sy) + "px; width:" + w + "px; height:22px";
            vec_11_el.style.cssText = pos11;
            vec_21_el.style.cssText = pos21;
        },

        /// compute normal from p0 and p1
        ///
        /// \param[in]  p0   point 0
        /// \param[in]  p1   point 1
        /// \param[out] nOrg normal origin position
        /// \param[out] nDir normal diretcion ([0,0,-1] when degenerated)
        computeNormal: function(p0, p1, nOrg, nDir) {
            // normal degeneration criterion
            var minimalNormalLength = 0.1;

            // normal origin = 0.5 * (p0 + p1)
            hyVector3.add(p0, p1, nOrg);
            hyVector3.scalarMult(0.5, nOrg, nOrg);
            // normalVec = normalize(rotate90(p1 - p0))
            hyVector3.subtract(p1, p0, nDir);
            var isNormalExist = (nDir.euclidian_length() >= minimalNormalLength) ? true : false;
            if(isNormalExist){
                // rotate90 = [0 -1; 1 0];
                var vx = -nDir.get(1);
                var vy =  nDir.get(0);
                nDir.set(0, vx);
                nDir.set(1, vy);
                nDir.set(2, 0.0);
                nDir.normalize();
            }
            else{
                nDir.set(0,  0.0);
                nDir.set(1,  0.0);
                nDir.set(2, -1.0);
                console.log("normal degenerated")
            }
        }

    });
    tangle.setValue("p1x", 2);
});



//----------------------------------------------------------
//  TKNormalTransformCanvas. control and view.
//    2D line and its normal visualization
Tangle.classes.TKNormalTransformCanvas = {

    /// initialize view
    initialize: function (element, options, tangle, p1x, p1y) {
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

        //----------------------------------------------------------------------
        // model to view matrix
        var sx =  this.vdat.canvas.width  / 8.0;
        var sy = -this.vdat.canvas.height / 8.0; // the screen coordinate is upside down.
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

        // model to view
        this.vdat.modelToViewMat = new hyMatrix33();
        hyMatrix33.multiply(transmat, scalemat, this.vdat.modelToViewMat);
        // model to screen
        this.vdat.modelToScreenMat = new hyMatrix33();
        this.vdat.modelToScreenMat.setEye(); // model x view x manipuration matrix
        var tmpmat = new hyMatrix33;
        tmpmat.setEye();
        hyMatrix33.multiply(this.vdat.modelToViewMat, tmpmat, this.vdat.modelToScreenMat);
        // screen to model
        this.vdat.screenToModelMat = new hyMatrix33();
        this.vdat.modelToScreenMat.inv(this.vdat.screenToModelMat);
        console.log("modelToViewMat: " + this.vdat.modelToViewMat);
        // var p0 = this.vdat.tangle.getValue("p0");
        // var p1 = this.vdat.tangle.getValue("p1");
        var p0 = new hyVector3([ 0, 0, 1]);
        var p1 = new hyVector3([ 2, 2, 1]);
        // p0v3 model p0's vector 3 form. p0v3ScrPos is its screen position
        this.vdat.p0v3       = p0.clone();
        this.vdat.p1v3       = p1.clone();
        this.vdat.p0v3ScrPos = new hyVector3();
        this.vdat.p1v3ScrPos = new hyVector3();
        this.vdat.modelToScreenMat.transformPoint(this.vdat.p0v3, this.vdat.p0v3ScrPos);
        this.vdat.modelToScreenMat.transformPoint(this.vdat.p1v3, this.vdat.p1v3ScrPos);

        this.vdat.p0Info = { x:this.vdat.p0v3ScrPos.get(0), y:this.vdat.p0v3ScrPos.get(1), radius:8, label:'0' };
        this.vdat.p1Info = { x:this.vdat.p1v3ScrPos.get(0), y:this.vdat.p1v3ScrPos.get(1), radius:8, label:'p' };

        //----------------------------------------------------------------------
        // mouse down point
        this.vdat.pointer_start_v3 = new hyVector3([0, 0, 1]);

        var vdRef = this.vdat;

        // background image
        this.vdat.coordinateBg = new Image();
        this.vdat.coordinateBg.onload = function(){
            // trigger update() and redraw canvas (are there better way than this hack?)
            var p0x = vdRef.tangle.getValue("p0x");
            vdRef.tangle.setValue("p0x", p0x + 0.0001);
            vdRef.tangle.setValue("p0x", p0x);
        };
        this.vdat.coordinateBg.src  = 'Image/coordinate_system.png';

        // Setup dragging using BVTouchable
        new BVTouchable(element, {
            touchDidGoDown: function (touches) {
                vdRef.pointer_start_v3.set(0, touches.event.client.x - vdRef.canvas.offsetParent.offsetLeft);
                vdRef.pointer_start_v3.set(1, touches.event.client.y - vdRef.canvas.offsetParent.offsetTop);

                // Is any point near to the mouse down point?
                var snap_rad_px = 6;
                var obj = {};
                console.log('touchDidGoDown');
                var p0ScrPos = new hyVector3();
                var p1ScrPos = new hyVector3();
                vdRef.modelToScreenMat.transformPoint(vdRef.p0v3, p0ScrPos);
                vdRef.modelToScreenMat.transformPoint(vdRef.p1v3, p1ScrPos);
                console.log('push at:' + vdRef.pointer_start_v3 +
                            ', p0v3: ' + vdRef.p0v3 + ' -> p0ScrPos: ' + p0ScrPos +
                            ', p1v3: ' + vdRef.p1v3 + ' -> p1ScrPos: ' + p1ScrPos);

                if(hyVector3.hypot(p0ScrPos, vdRef.pointer_start_v3) < snap_rad_px){
                    vdRef.isDragging = true;
                    vdRef.isDraggingPoint = '0';
                    console.log('drag on p0');
                    // get screen to model coordinate
                    vdRef.screenToModelMat.transformPoint(vdRef.pointer_start_v3, vdRef.p0v3);
                    obj['p0x'] = vdRef.p0v3.get(0);
                    obj['p0y'] = vdRef.p0v3.get(1);
                    tangle.setValues(obj);
                    console.log('drag on p0.' + vdRef.p0v3);
                }
                else if(hyVector3.hypot(p1ScrPos, vdRef.pointer_start_v3) < snap_rad_px){
                    vdRef.isDragging = true;
                    vdRef.isDraggingPoint = '1';
                    // get screen to model coordinate
                    vdRef.screenToModelMat.transformPoint(vdRef.pointer_start_v3, vdRef.p1v3);
                    obj['p1x'] = vdRef.p1v3.get(0);
                    obj['p1y'] = vdRef.p1v3.get(1);
                    tangle.setValues(obj);
                    console.log('drag on p1. ' + vdRef.p1v3);
                }
                else{
                    console.log('no near point. v0:' + vdRef.p0v3);
                    vdRef.isDragging = false;
                }
            },
            touchDidMove: function (touches) {
                console.log('touchDidMove:' + vdRef.isDragging);
                if(!vdRef.isDragging){
                    return;
                }
                // var pointer_x = vdRef.pointer_start_v3.get(0) + touches.translation.x;
                // var pointer_y = vdRef.pointer_start_v3.get(1) - touches.translation.y;
                var cur_point = new hyVector3();
                cur_point.set(0, vdRef.pointer_start_v3.get(0) + touches.translation.x);
                cur_point.set(1, vdRef.pointer_start_v3.get(1) - touches.translation.y);
                cur_point.set(2, 1);
                var obj = {}
                if(vdRef.isDraggingPoint == '0'){
                    vdRef.screenToModelMat.transformPoint(cur_point, vdRef.p0v3);
                    obj['p0x'] = vdRef.p0v3.get(0);
                    obj['p0y'] = vdRef.p0v3.get(1);
                    tangle.setValues(obj);
                    console.log("BVTouchable: touchDidMove:0 "  + cur_point + " -> " + vdRef.p0v3);
                }
                else if(vdRef.isDraggingPoint == '1'){
                    vdRef.screenToModelMat.transformPoint(cur_point, vdRef.p1v3);
                    obj['p1x'] = vdRef.p1v3.get(0);
                    obj['p1y'] = vdRef.p1v3.get(1);
                    tangle.setValues(obj);
                    console.log("BVTouchable: touchDidMove:1 "  + cur_point + " -> " + vdRef.p1v3);
                }
                else{
                    throw new Error("No such dragging point.");
                }
            },
            touchDidGoUp: function (touches) {
                // console.log("BVTouchable: touchDidGoUp")
                // var pointer_x = vdRef.pointer_start_v3.get(0) + touches.translation.x;
                // var pointer_y = vdRef.pointer_start_v3.get(1) - touches.translation.y;
                if(!vdRef.isDragging){
                    return;
                }

                var cur_point = new hyVector3();
                cur_point.set(0, vdRef.pointer_start_v3.get(0) + touches.translation.x);
                cur_point.set(1, vdRef.pointer_start_v3.get(1) - touches.translation.y);
                cur_point.set(2, 1);
                var obj = {}

                if(vdRef.isDraggingPoint == '0'){
                    vdRef.screenToModelMat.transformPoint(cur_point, vdRef.p0v3);
                    obj['p0x'] = vdRef.p0v3.get(0);
                    obj['p0y'] = vdRef.p0v3.get(1);
                    tangle.setValues(obj);
                }
                else if(vdRef.isDraggingPoint == '1'){
                    vdRef.screenToModelMat.transformPoint(cur_point, vdRef.p1v3);
                    obj['p1x'] = vdRef.p1v3.get(0);
                    obj['p1y'] = vdRef.p1v3.get(1);
                    tangle.setValues(obj);
                }
                else{
                    throw new Error("No such dragging point.");
                }
                vdRef.isDragging = false;
            }
        });                     // new BVTouchable
    },                          // initialize function

    /// update the view
    update: function (el, scale_x) {
        //  console.log("canvas update: ");

        // this.getNormalInScreenCoords();
        // this.updateNormalWithTranslation();

        this.drawCanvas(el);
    },                      // update function

    /// draw the whole canvas
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

        var manipmat = this.vdat.tangle.getValue("manipMat");
        hyMatrix33.multiply(this.vdat.modelToViewMat, manipmat, this.vdat.modelToScreenMat);
        this.vdat.modelToScreenMat.inv(this.vdat.screenToModelMat);

        this.vdat.p0v3ScrPos = this.vdat.modelToScreenMat.transformPoint(p0);
        this.vdat.p1v3ScrPos = this.vdat.modelToScreenMat.transformPoint(p1);

        // console.log("update: " + this.vdat.p0v3 + "\n" + this.vdat.p1v3);

        // draw the plane
        this.drawPlane(ctx, this.vdat.p0v3ScrPos, this.vdat.p1v3ScrPos);

        // draw the handle point
        this.vdat.p0Info.x = this.vdat.p0v3ScrPos.get(0);
        this.vdat.p0Info.y = this.vdat.p0v3ScrPos.get(1);
        this.vdat.p1Info.x = this.vdat.p1v3ScrPos.get(0);
        this.vdat.p1Info.y = this.vdat.p1v3ScrPos.get(1);
        this.drawHanlePoint(ctx, this.vdat.p0Info);
        this.drawHanlePoint(ctx, this.vdat.p1Info);

        // draw the translated normal (show the wrong case)
        var nOrg = this.vdat.tangle.getValue("normalOrigin");
        var nDir = this.vdat.tangle.getValue("normalDir");
        var nEnd = new hyVector3(); // FIXME: new every time
        this.pointAdd(nOrg, nDir, nEnd);
        var nOrgScr = this.vdat.modelToScreenMat.transformPoint(nOrg);
        var nEndScr = this.vdat.modelToScreenMat.transformPoint(nEnd);
        this.drawNormal(ctx, nOrgScr, nEndScr, nDir);

        // draw the correct normal
        var nOrg = this.vdat.tangle.getValue("normalOrigin");
        var nDir = this.vdat.tangle.getValue("normalDir");
        var nEnd = new hyVector3(); // FIXME: new every time
        this.pointAdd(nOrg, nDir, nEnd);
        var nOrgScr = this.vdat.modelToScreenMat.transformPoint(nOrg);
        var nEndScr = this.vdat.modelToScreenMat.transformPoint(nEnd);
        this.drawNormal(ctx, nOrgScr, nEndScr, nDir);

    },

    /// point addition (homogeneous coordinates)
    pointAdd: function(p0v3, p1v3, pret){
        hyVector3.add(p0v3, p1v3, pret);
        pret.set(2, 1);
    },

    /// draw the plane (a line, in this example)
    ///
    /// \param[in] ctx context of the 2d canvas
    /// \param[in] p0  line start point (3 length float array, homogenious coordinates)
    /// \param[in] p1  line end point   (3 length float array, homogenious coordinates)
    drawPlane: function(ctx, p0, p1) {
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.strokeStyle = '#0f0f0f';
        ctx.moveTo(p0.get(0), p0.get(1));
        ctx.lineTo(p1.get(0), p1.get(1));
        ctx.stroke();
        ctx.closePath();
    },

    /// draw the handle point (a point with a label and some size)
    ///
    /// \param[in] ctx context of the 2d canvas
    /// \param[in] pointInfo handle point information
    /// pointInfo = {
    ///   x: handle point center x coordinate,
    ///   y: handle point center y coordinate,
    ///   radius: handle point radius,
    ///   label:  handle point label (assumes one charactor)
    /// };
    drawHanlePoint: function(ctx, pointInfo) {
        ctx.fillStyle = "#ff0000";
        ctx.beginPath();
        ctx.arc(pointInfo.x, pointInfo.y, pointInfo.radius, 0, Math.PI*2, true);
        ctx.closePath();
        ctx.fill();
        ctx.fillStyle = "#FFFFFF";
        ctx.fillText(pointInfo.label, pointInfo.x - 3, pointInfo.y + 4);
        if(this.vdat.isDragging){
            ctx.fillStyle = "#444444";
            // FIXME: currently print the screen coordinates.
            posstr = sprintf("[%.1f:%.1f]", pointInfo.x, pointInfo.y);
            ctx.fillText(posstr, pointInfo.x + pointInfo.radius + 2, pointInfo.y + pointInfo.radius + 2);
        }
    },

    /// draw the normal
    ///
    /// points are 3 length float array, homogenious coordinates.
    ///
    /// \param[in] ctx context of the 2d canvas
    /// \param[in] p0  line start point in the screen coordinates
    /// \param[in] p1  line end   point in the screen coordinates
    /// \param[in] nnormalDir normal direction. degenerated when [0,0,-1].
    drawNormal: function(ctx, p0, p1, normalDir) {
        if(normalDir.get(2) == -1){
            ctx.fillStyle = "#cc2222";
            ctx.fillText("Normal degenerated",
                         this.vdat.canvas.width  - 100,
                         this.vdat.canvas.height - 30);
            return;
        }
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.strokeStyle = '#0f0f0f';
        ctx.moveTo(p0.get(0), p0.get(1));
        ctx.lineTo(p1.get(0), p1.get(1));
        ctx.stroke();
        ctx.closePath();
        // ctx.fillStyle = "#888888";
        // ctx.fillText("normal", p0.m_element[0] + 4, p0.m_element[1] + 4);
    }
};                              // TKNormalTransformCanvas

})();
