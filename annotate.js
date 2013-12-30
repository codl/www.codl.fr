window.onload = function(){
    "use strict";
    var els = document.querySelectorAll(".annotate, abbr");
    for(var i = 0; i < els.length; i++){
        var el = els[i];
        el.classList.add("active");
        var title = el.title;
        el.title = "";
        (function(title, parentel){
            var el = null;
            function show(e){
                if(el) return; // let hide() be triggered
                e.stopPropagation();
                el = document.createElement("div");
                el.classList.add("annotation");
                el.appendChild(document.createTextNode(title));
                parentel.appendChild(el);
            }
            function hide(){
                if(!el) return;
                parentel.removeChild(el);
                el = null;
            }
            parentel.addEventListener("click", show);
            parentel.addEventListener("touch", show);
            window.addEventListener("click", hide);
        })(title, el);


    }
}
