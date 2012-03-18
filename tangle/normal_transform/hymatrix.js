//
//  hymatrix.js
//
//  A simple matrix class for explanations
//  (C) 2012 Hitoshi Yamauchi.  New BSD license.
//
//  Maybe there are many vector classes, so put hy as a prefix.
//

// something like C++ assertion
var HYMATRIX_IS_DEBUG = true;

if(HYMATRIX_IS_DEBUG){
    function hyMatrixAssert(cond, msg) {
        if(!cond){
            throw new Error("Assertion failed: " + msg);
        }
    }
}
else{
    function hyMatrixAssert(cond, msg) {
        // empty
    }
}


/// constructor of hyMatrix33.
/// \param[in] elem initial elements of length 3x3. Or may be undefined.
function hyMatrix33(elem){
    if(elem == null){
        this.m_element = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
    }
    else if((elem.length != 3)    && (elem[0].length == 3) &&
            (elem[1].length == 3) && (elem[2].length == 3)){
        throw new Error("invalid array length for hyMatrix33.");
    }
    else {
        this.m_element = new Array(3);
        this.m_element[0] = new Array(3);
        this.m_element[1] = new Array(3);
        this.m_element[2] = new Array(3);
        for(var j = 0; j < 3; j++){
            for(var i = 0; i < 3; i++){
                if(i == j){
                    this.m_element[i][j] = 1;
                }else{
                    this.m_element[i][j] = 0;
                }
            }
        }
    }
}

/// get string representation of hyVector3
hyMatrix33.prototype.toString = function(){
    var ret = new String();
    for(var j = 0; j < 3; j++){
        for(var i = 0; i < 3; i++){
            ret += this.m_element[i][j] + " ";
        }
        ret += "\n";
    }
    return ret;
}

/// set zero
hyMatrix33.prototype.setZero = function(){
    for(var j = 0; j < 3; j++){
        for(var i = 0; i < 3; i++){
            this.m_element[i][j] = 0;
        }
    }
}

/// set identity
hyMatrix33.prototype.setEye = function(){
    this.setZero();
    for(var i = 0; i < 3; i++){
        this.m_element[i][i] = 1;
    }
}

/// set translate 2d
///
/// \param[in] tx translation x
/// \param[in] ty translation y
hyMatrix33.prototype.setTranslation2D = function(tx, ty){
    this.m_element[2][0] = tx;
    this.m_element[2][1] = ty;
}

/// set scale 2d
///
/// \param[in] sx scaling x
/// \param[in] sy scaling y
hyMatrix33.prototype.setScale2D = function(sx, sy){
    this.m_element[0][0] = sx;
    this.m_element[1][1] = sy;
}

/// set rotation 2d
///
/// \param[in] theta rotation angle
hyMatrix33.prototype.setRotation2D = function(theta){
    this.m_element[0][0] =  Math.cos(theta);
    this.m_element[0][1] = -Math.sin(theta);
    this.m_element[1][0] =  Math.sin(theta);
    this.m_element[1][1] =  Math.cos(theta);
}

/// matrix multiplication
///
hyMatrix33.prototype.multiply = function(m0, m1, m2){
    if(m2 == null){
        m2 = new hyMatrix33();
    }
    m2.setZero();

    for(var i = 0; i < 3; i++){
        for(var j = 0; j < 3; j++){
            for(var k = 0; k < 3; k++){
                // note: reversed from math notation
                m2.m_element[j][i] += m0.m_element[k][i] * m1.m_element[j][k];
            }
        }
    }
    return m2;
}

/// transform point
///
hyMatrix33.prototype.transformPoint = function(v0, v1){
    hyMatrixAssert((v0 instanceof hyVector3),
                   "hyMatrix33.prototype.transformPoint: v0 is not hyMatrix33.");
    if(v1 == null){
        v1 = new hyVector3();
    }

    for(var i = 0; i < 3; i++){
        v1.m_element[i] = 0;
        for(var j = 0; j < 3; j++){
            v1.m_element[i] += this.m_element[j][i] * v0.m_element[j];
        }
    }
    return v1;
}


