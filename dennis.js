$(function($){
    var we_have_dennis = false;
    function dennis(){
        if(we_have_dennis) return;

        ga('send', 'event', 'dennis', 'dennis');

        we_have_dennis = true;

        var audio = $('<audio/>', { src: '/dennis.ogg', loop: true })[0];
        audio.style.display = 'none';
        $("pre").after(audio);
        audio.play();
        $("html").addClass("dennis");
    }
    $('#dennis').on('click', dennis);
});
