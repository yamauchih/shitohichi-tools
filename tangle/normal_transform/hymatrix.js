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
        // print("hyMatrix33: elem is null.");
        this.m_elem = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
    }
    else if((elem.length != 3)    && (elem[0].length == 3) &&
            (elem[1].length == 3) && (elem[2].length == 3)){
        throw new Error("invalid array length for hyMatrix33.");
    }
    else {
        this.m_elem = new Array(3);
        this.m_elem[0] = new Array(3);
        this.m_elem[1] = new Array(3);
        this.m_elem[2] = new Array(3);
        for(var j = 0; j < 3; j++){
            for(var i = 0; i < 3; i++){
                this.m_elem[i][j] = elem[i][j];
            }
        }
    }
}

//----------------------------------------------------------------------
// instance methods
//----------------------------------------------------------------------

/// clone this
hyMatrix33.prototype.clone = function(){
    var newMat = new hyMatrix33();
    for(var j = 0; j < 3; j++){
        for(var i = 0; i < 3; i++){
            newMat.m_elem[i][j] = this.m_elem[i][j];
        }
    }
    return newMat;
}

/// get element
hyMatrix33.prototype.get = function(i, j){
    return this.m_elem[j][i];
}

/// set element
hyMatrix33.prototype.set = function(i, j, val){
    this.m_elem[j][i] = val;
}


/// get string representation of this
hyMatrix33.prototype.toString = function(){
    var ret = new String();
    for(var j = 0; j < 3; j++){
        for(var i = 0; i < 3; i++){
            ret += this.get(i, j) + " ";
        }
        ret += "\n";
    }
    return ret;
}

/// set this zero marix
hyMatrix33.prototype.setZero = function(){
    for(var j = 0; j < 3; j++){
        for(var i = 0; i < 3; i++){
            this.set(i, j, 0);
        }
    }
}

/// set this identity matrix
hyMatrix33.prototype.setEye = function(){
    this.setZero();
    for(var i = 0; i < 3; i++){
        this.set(i, i, 1);
    }
}

/// multiply a scalar for all components
/// \param[in] scalar a scalar to multiply
hyMatrix33.prototype.multScalar = function(scalar){
    for(var i = 0; i < 3; i++){
        for(var j = 0; j < 3; j++){
            this.m_elem[i][j] *= scalar;
        }
    }
}

/// set translate 2d
///
/// \param[in] tx translation x
/// \param[in] ty translation y
hyMatrix33.prototype.setTranslation2D = function(tx, ty){
    this.set(0, 2, tx);
    this.set(1, 2, ty);
}

/// set scale 2d
///
/// \param[in] sx scaling x
/// \param[in] sy scaling y
hyMatrix33.prototype.setScale2D = function(sx, sy){
    this.set(0, 0, sx);
    this.set(1, 1, sy);
}

/// set rotation 2d
///
/// \param[in] theta rotation angle
hyMatrix33.prototype.setRotation2D = function(theta){
    this.set(0, 0,  Math.cos(theta));
    this.set(0, 1,  Math.sin(theta));
    this.set(1, 0, -Math.sin(theta));
    this.set(1, 1,  Math.cos(theta));
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
        v1.m_elem[i] = 0;
        for(var j = 0; j < 3; j++){
            v1.m_elem[i] += this.m_elem[j][i] * v0.m_elem[j];
        }
    }
    return v1;
}


/// determinant
/// \return determinant
hyMatrix33.prototype.det = function(){
    var det = (+ this.get(0,0) * this.get(1,1) * this.get(2,2)
               + this.get(1,0) * this.get(2,1) * this.get(0,2)
               + this.get(2,0) * this.get(0,1) * this.get(1,2)
               - this.get(0,0) * this.get(1,2) * this.get(2,1)
               - this.get(1,0) * this.get(0,1) * this.get(2,2)
               - this.get(2,0) * this.get(1,1) * this.get(0,2));
    return det;
}


/// inverse
/// \param[in] invmat (optional)if given inverse matrix is computed on
/// invmat, else result matrix is newed.
/// \return inv matrix
hyMatrix33.prototype.inv = function(invmat){
    var det = this.det();
    if(det == 0.0){
        throw new Error("inv: Singular matrix.");
    }
    var invdet = 1.0/det;

    if(invmat == null){
        invmat = new hyMatrix33();
    }

    // cofactor^T
    invmat.set(0,0, + (this.get(1,1) * this.get(2,2) - this.get(1,2) * this.get(2,1)));
    invmat.set(1,0, - (this.get(1,0) * this.get(2,2) - this.get(1,2) * this.get(2,0)));
    invmat.set(2,0, + (this.get(1,0) * this.get(2,1) - this.get(1,1) * this.get(2,0)));
    invmat.set(0,1, - (this.get(0,1) * this.get(2,2) - this.get(2,1) * this.get(0,2)));
    invmat.set(1,1, + (this.get(0,0) * this.get(2,2) - this.get(2,0) * this.get(0,2)));
    invmat.set(2,1, - (this.get(0,0) * this.get(2,1) - this.get(2,0) * this.get(0,1)));
    invmat.set(0,2, + (this.get(0,1) * this.get(1,2) - this.get(1,1) * this.get(0,2)));
    invmat.set(1,2, - (this.get(0,0) * this.get(1,2) - this.get(1,0) * this.get(0,2)));
    invmat.set(2,2, + (this.get(0,0) * this.get(1,1) - this.get(0,1) * this.get(1,0)));

    invmat.multScalar(invdet);

    return invmat;
}

//----------------------------------------------------------------------
// class methods
//----------------------------------------------------------------------

/// matrix multiplication
///
hyMatrix33.multiply = function(m0, m1, m2){
    if(m2 == null){
        m2 = new hyMatrix33();
    }
    if(m1 == m2){
        throw new Error("Can not override m2 since it is the same object with m1. (m2 will be zero.)");
    }
    m2.setZero();

    for(var i = 0; i < 3; i++){
        for(var j = 0; j < 3; j++){
            for(var k = 0; k < 3; k++){
                // note: reversed from math notation
                m2.m_elem[j][i] += m0.m_elem[k][i] * m1.m_elem[j][k];
            }
        }
    }
    return m2;
}

//----------------------------------------------------------------------
// class property
//----------------------------------------------------------------------

hyMatrix33.name = "hyMatrix33";

