window.onload = init;
function init() {
    var xhr = new XMLHttpRequest(); //for json file info
    var bracketJSON = '../../data.json';
    var brObj;
    var startup = true;
    var animated = false;
    var cBust = 0;

    function pollJSON() {
        xhr.open('GET', bracketJSON + '?v=' + cBust, true);
        xhr.send();
        cBust++;
    }

    pollJSON();
    setInterval(function () { pollJSON(); }, 500);

    xhr.onreadystatechange = parseJSON;

    function parseJSON() {
        if (xhr.readyState === 4) {
            brObj = JSON.parse(xhr.responseText);
            if (animated == true) {
                bracket();
            }
        }
    }



    function bracket() {
        if (startup == true) {
           /* var video = document.getElementById('bracketVid');
            video.src = '../webm/top8_bracket.webm';

            video.muted = true;
            video.play();

            function pauseVid() {
                video.pause();
            }

            setTimeout(pauseVid, 7000);*/

            getData();
            startup = false;
            animated = true;
        }
        getData();
    }
    setTimeout(bracket, 300);

    function getData() {
        var x;
        if (startup == true) {
            for (x of brObj) {
                var p1Name = x.player1;
                var p2Name = x.player2;
                var p1Score = x.p1Score;
                var p2Score = x.p2Score;

                TweenMax.set('#' + x.id + '_p1_name', { css: { x: namemove } });
                TweenMax.set('#' + x.id + '_p2_name', { css: { x: namemove } });

                $('#' + x.id + '_p1_name').html(p1Name);
                $('#' + x.id + '_p2_name').html(p2Name);
                $('#' + x.id + '_p1_score').html(p1Score);
                $('#' + x.id + '_p2_score').html(p2Score);

                resize(x.id + '_p1_name');
                resize(x.id + '_p2_name');

                TweenMax.to('#' + x.id + '_p1_name', nametime, { css: { x: '+0px', opacity: 1 }, ease: Quad.easeOut, delay: namedelay });
                TweenMax.to('#' + x.id + '_p2_name', nametime, { css: { x: '+0px', opacity: 1 }, ease: Quad.easeOut, delay: namedelay });
                TweenMax.to('#' + x.id + '_p1_score', brtime, { css: { opacity: 1 }, ease: Quad.easeOut, delay: brdelay });
                TweenMax.to('#' + x.id + '_p2_score', brtime, { css: { opacity: 1 }, ease: Quad.easeOut, delay: brdelay });


                if (x.id == "gf_1") {
                    break; //challonge has two grand finals for grand finals reset
                }
            }
        }
        else {
            for (x of brObj) {
                var p1Name = x.player1;
                var p2Name = x.player2;
                var p1Score = x.p1Score;
                var p2Score = x.p2Score;

                name_update(x.id + '_p1_name', p1Name);
                name_update(x.id + '_p2_name', p2Name);

                score_update(x.id + '_p1_score', p1Score);
                score_update(x.id + '_p2_score', p2Score);

                if (x.id == "gf_1") {
                    break; //challonge has two grand finals for grand finals reset
                    //going into the second gf causes and infinite update loop
                }
            }
        }
    }

    function score_update(ID, score) {
        if ($('#' + ID).text() != score) {
            TweenMax.to(('#' + ID), .3, {
                css: { opacity: 0 }, ease: Quad.easeout, delay: 0, onComplete: function () {
                    $('#' + ID).html(score);


                    TweenMax.to('#' + ID, .3, { css: { opacity: 1 }, ease: Quad.easeOut, delay: .2 });
                }
            })
        }
    }

    function name_update(ID, name) {
        wrap = $('#' + ID);
        if ($('#' + ID).text() != name ) {
            TweenMax.to('#' + ID, .3, {
                css: { x: namemove, opacity: 0 }, ease: Quad.easeout, delay: 0, onComplete: function () {
                    $('#' + ID).css('font-size', namesize);
                    $('#' + ID).html(name);

                    resize(ID); 

                    TweenMax.to('#' + ID, .3, { css: { x: '+0px', opacity: 1 }, ease: Quad.easeOut, delay: .2 });
                }
            })
        }
    }

    function resize(ID) { //makes the name fit in the space
        wrap = $('#' + ID);

        wrap.each(function (i, wrap) { //function to resize font if text string is too long and causes div to overflow its width/height boundaries
            while (wrap.scrollWidth > wrap.offsetWidth || wrap.scrollHeight > wrap.offsetHeight) {
                var newFontSize = (parseFloat($(wrap).css('font-size').slice(0, -2)) * .95) + 'px';
                $(wrap).css('font-size', newFontSize);
            }
        });
    }
}