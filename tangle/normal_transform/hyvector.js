//
//  hyvector.js
//
//  A simple vector/matrix class for explanations
//  (C) 2012 Hitoshi Yamauchi.  New BSD license.
//
//  Maybe there are many vector classes, so put hy as a prefix.
//

/// something like C++ assertion
var HYVECTOR_IS_DEBUG = true;
if(HYVECTOR_IS_DEBUG){
    function hyVectorAssert(cond, msg) {
        if(!cond){
            // if you forget the assertion message, you will get
            // "Assertion failed: undefined".
            throw new Error("Assertion failed: " + msg);
        }
    }
}
else{
    function hyVectorAssert(cond, msg) {
        // empty
    }
}

/// constructor of hyVector3.
/// \param[in] elem initial elements of length 3. Or may be undefined.
function hyVector3(elem){
    if(elem == null){
        this.m_element = [0, 0, 0];
    }
    else if(elem.length != 3){
        throw new Error("invalid array length for hyVector3.");
    }
    else {
        this.m_element = new Array(3);
        this.m_element[0] = elem[0];
        this.m_element[1] = elem[1];
        this.m_element[2] = elem[2];
    }
}

//----------------------------------------------------------------------
// instance methods
//----------------------------------------------------------------------

/// clone this
///
///   hyVector3.prototype is prototype of each instance. (You need an
///   instance to call. This clone needs this, therefore, prototype.)
///
///   hyVector3.clone     is class method (like a static method)
hyVector3.prototype.clone = function(){
    return new hyVector3([this.m_element[0], this.m_element[1], this.m_element[2]]);
}

/// get string representation of hyVector3
hyVector3.prototype.toString = function(){
    return this.m_element[0] + " "
        + this.m_element[1] + " " + this.m_element[2];
}

/// squared length
hyVector3.prototype.sqrLength = function(){
    var sqrlen = (this.m_element[0] * this.m_element[0]) +
        (this.m_element[1] * this.m_element[1]) + (this.m_element[2] * this.m_element[2]);
    return sqrlen;
}

/// euclidian length. (Note: length is preserved.)
hyVector3.prototype.euclidian_length = function(){
    return Math.sqrt(this.sqrLength());
}

/// normalize this vector.
/// This changes the this instance, therefore, use prototype.
hyVector3.prototype.normalize = function(){
    var sqrlen = this.sqrLength(this);
    if(sqrlen == 0.0){
        throw new Error("Cannot normalize zero length vector.");
    }
    var len = Math.sqrt(sqrlen);

    this.m_element[0] /= len;
    this.m_element[1] /= len;
    this.m_element[2] /= len;

    return this;
}


//----------------------------------------------------------------------
// class methods
//----------------------------------------------------------------------

/// add two hyVector3. When vret is not null, reuse the vret without new.
hyVector3.add = function(v0, v1, vret){
    if(vret == null){
        vret = new hyVector3();
    }
    hyVectorAssert(v0.m_element.length == 3,   "hyVector3.add: should be v0.m_element.length == 3");
    hyVectorAssert(v1.m_element.length == 3,   "hyVector3.add: should be v1.m_element.length == 3");
    hyVectorAssert(vret.m_element.length == 3, "hyVector3.add: should be vret.m_element.length == 3");

    vret.m_element[0] = v0.m_element[0] + v1.m_element[0];
    vret.m_element[1] = v0.m_element[1] + v1.m_element[1];
    vret.m_element[2] = v0.m_element[2] + v1.m_element[2];

    return vret;
}

/// subtract two hyVector3. When vret is not null, reuse the vret without new.
hyVector3.subtract = function (v0, v1, vret){
    if(vret == null){
        vret = new hyVector3();
    }
    hyVectorAssert(v0.m_element.length == 3,   "hyVector3.subtract: should be v0.m_element.length == 3");
    hyVectorAssert(v1.m_element.length == 3,   "hyVector3.subtract: should be v1.m_element.length == 3");
    hyVectorAssert(vret.m_element.length == 3, "hyVector3.subtract: should be vret.m_element.length == 3");

    vret.m_element[0] = v0.m_element[0] - v1.m_element[0];
    vret.m_element[1] = v0.m_element[1] - v1.m_element[1];
    vret.m_element[2] = v0.m_element[2] - v1.m_element[2];

    return vret;
}

/// multiply a scalar
hyVector3.scalarMult = function hyVector3_scalarMult(s0, v0, vret){
    if(vret == null){
        vret = new hyVector3();
    }
    hyVectorAssert(v0.m_element.length == 3,   "hyVector3.scalarMult: should be v0.m_element.length == 3");

    vret.m_element[0] = s0 * v0.m_element[0];
    vret.m_element[1] = s0 * v0.m_element[1];
    vret.m_element[2] = s0 * v0.m_element[2];

    return vret;
}

/// comparison method. true when all the elements are the same.
hyVector3.equal = function hyVector3_equal(v0, v1){
    hyVectorAssert(v0.m_element.length == 3,   "hyVector3.add: should be v0.m_element.length == 3");
    hyVectorAssert(v1.m_element.length == 3,   "hyVector3.add: should be v1.m_element.length == 3");

    if((v0.m_element[0] == v1.m_element[0]) &&
       (v0.m_element[1] == v1.m_element[1]) &&
       (v0.m_element[2] == v1.m_element[2])){
        return true;
    }
    return false;
}


