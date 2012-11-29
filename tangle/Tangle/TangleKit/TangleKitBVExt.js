//
//  TangleKitBVExt.js
//
//  Bret Victor's TangleKit extension
//  (C) 2012 Bret Victor.
//


(function () {

//----------------------------------------------------------------------
//
// TkExpandingList (http://worrydream.com/Tangle/pants.html)
//
Tangle.classes.TkExpandingList = {
    initialize: function (element, options, tangle, variable) {
        var isExpanded = false;
        var items = options.items.split("/");

        var subelements = [];
        subelements.push(new Element("span", { text:"[ " }));
        items.each(function (item, index) {
            var itemElement = new Element("span", { "class":"TkExpandingListItem", text:item });
            itemElement.onclick = function () { itemWasClicked(item); }
            subelements.push(itemElement);
            if (index < items.length - 1) {
                subelements.push(new Element("span", { text:", " }));
            }
        });
        subelements.push(new Element("span", { text:" ]" }));

        subelements.each(function (subelement) { subelement.inject(element, "bottom"); });

        function itemWasClicked (item) {
            isExpanded = !isExpanded;
            tangle.setValue(variable, item);
            update(element,item);  // update expanded, even if variable doesn't change
        }

        function update (element, value) {
            subelements.each(function (subelement) {
                var text = subelement.get("text");
                subelement.style.display = (isExpanded || text == value) ? "inline" : "none";
            });
        }
        this.update = update;
    }
};

//----------------------------------------------------------------------

})();

