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
    va = new hyVector3([1,2,3]);
    vb = new hyVector3([4,5,6]);
    vc = new hyVector3();
    // print("va, vb, vc = [" + va + "], [" + vb + "], [" + vc + "]");
    // print(va.m_element.length);
    hyVector3.add(va, vb, vc);
    hyVectorAssert(hyVector3.equal(vc, new hyVector3([5,7,9])), "add().");
    hyVector3.subtract(va, vb, vc);
    hyVectorAssert(hyVector3.equal(vc, new hyVector3([-3,-3,-3])), "subtract().");
    // print("va, vb, vc = [" + va + "], [" + vb + "], [" + vc + "]");
    hyVectorAssert(va.sqrLength() == 14,                   "sqrLength");
    // print(hyVector3.euclidian_length(va));
    hyVectorAssert(va.euclidian_length() == Math.sqrt(14), "length");
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

    b = new hyMatrix33([[0.28069, 0.85918, 0.16456],
                        [0.14836, 0.26829, 0.95889],
                        [0.60733, 0.68177, 0.70212]]);
    print("b.det() = " + b.det() + "\n");
    c = new hyMatrix33();
    b.inv(c);
    print("b:\n" + b);
    print("expected c:\n-1.72320  -1.81831   2.88714\n" +
          "1.77067   0.35967  -0.90620\n-0.22880   1.22358  -0.19317\n");
    print("c:\n" + c);
    d = new hyMatrix33();
    hyMatrix33.multiply(b, c, d);
    print("d:\n" + d);
}

test_hymatrix();

