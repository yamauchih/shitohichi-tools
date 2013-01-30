//
//  ex08.js
//
//  A simple slider using Tangle (http://worrydream.com/Tangle/).
//  and TangleKitHYExt
//  (C) 2012 Hitoshi Yamauchi.  New BSD license.
//

(function () {

// MooTools: when DOM is ready, this is called
window.addEvent('domready', function () {

    // <div id="slider_example"> in ex08.html
    // This should contains all of this elements: canvas and point texts
    var container = document.getElementById("slider_example");
    var tangle = new Tangle(container, {
        initialize: function () {
            this.px = 10;
        },
        update: function () {
            console.log("tangle updated")
        }
    });
    tangle.setValue("px", 40);
});

})();
