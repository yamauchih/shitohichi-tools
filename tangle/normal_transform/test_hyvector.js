//
//  test_hyvector.js
//
//  A simple vector/matrix class for explanations
//  (C) 2012 Hitoshi Yamauchi.  New BSD license.
//
//  unit test for hyvector.
//
//  run:
//    rhino test_hyvector.js
//

load("hyvector.js");
load("hymatrix.js");

test_hyvector = function()
{
    a = new hyVector3();
    print(a);
}

test_hyvector();


test_hymatrix = function()
{
    a = new hyMatrix33();
    print("construct.\n" + a);

    a.setZero();
    print("setZero.\n" + a);
    a.setEye();
    print("setEye.\n" + a);
}

test_hymatrix();

