//
//  hyvector.js
//
//  A simple vector/matrix class for explanations
//  (C) 2012 Hitoshi Yamauchi.  New BSD license.
//
//  Maybe there are many vector classes, so put hy as a prefix.
//

// something like C++ assertion
var HYVECTOR_IS_DEBUG = true;

if(HYVECTOR_IS_DEBUG){
    function hyVectorAssert(cond, msg) {
        if(!cond){
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

/// clone this
hyVector3.prototype.clone = function(){
    return new hyVector3([this.m_element[0], this.m_element[1], this.m_element[2]]);
}


/// get string representation of hyVector3
hyVector3.prototype.toString = function(){
    return this.m_element[0] + " "
        + this.m_element[1] + " " + this.m_element[2];
}

/// add two hyVector3. When vret is not null, reuse the vret without new.
hyVector3.prototype.add = function(v0, v1, vret){
    if(vret == null){
        vret = new hyVector3();
    }
    hyVectorAssert(v0.lenth == 3,   "hyVector3.add: should be v0.lenth == 3");
    hyVectorAssert(v1.lenth == 3,   "hyVector3.add: should be v1.lenth == 3");
    hyVectorAssert(vret.lenth == 3, "hyVector3.add: should be vret.lenth == 3");

    vret[0] = v0[0] + v1[0];
    vret[1] = v0[1] + v1[1];
    vret[2] = v0[2] + v1[2];

    return vret;
}

/// subtract two hyVector3. When vret is not null, reuse the vret without new.
hyVector3.prototype.subtract = function(v0, v1, vret){
    if(vret == null){
        vret = new hyVector3();
    }
    hyVectorAssert(v0.lenth == 3,   "hyVector3.subtract: should be v0.lenth == 3");
    hyVectorAssert(v1.lenth == 3,   "hyVector3.subtract: should be v1.lenth == 3");
    hyVectorAssert(vret.lenth == 3, "hyVector3.subtract: should be vret.lenth == 3");

    vret[0] = v0[0] - v1[0];
    vret[1] = v0[1] - v1[1];
    vret[2] = v0[2] - v1[2];

    return vret;
}
