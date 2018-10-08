var limbMissing = false;
var interval = null;
var limbVisualIndex = false;
var resetCounter = 2;
var latestInjury = null;
function hideInjury() {
    $('.body-spot').hide();
}

function hideAdvice() {
    $('#injury-info-text-0').html('');
    $('#injury-info-container-0').hide();
    $('#injury-info-text-1').html('');
    $('#injury-info-container-1').hide();
    $('#injury-info-text-2').html('');
    $('#injury-info-container-2').hide();
}

function showInjury(data) {
    $('#body-spot-' + data.bodyPart).show();
}

function showLeftLimbMissing() {
    interval = setInterval(function() {
        limbVisualIndex = !limbVisualIndex;
        var imgUrl = !limbVisualIndex ? "../static/body_red_hand_v2.png" : "../static/body_red_hand_removed_v2.png";
        $("#body-figure").attr("src",imgUrl);
    }, 500);
}

function resetPerson() {
    limbMissing = false;
    limbVisualIndex = 0;
    if (interval) {
        clearInterval(interval);
        interval = null;
    }
    $("#body-figure").attr("src","../static/body2.png");
}

function getAdvice(data) {
    $.ajax({
        type:"POST",
        url: "http://localhost:5000/advice/?st="+JSON.stringify(data),
        success: function(data) {
            $('#injury-info-text').html(data);
            $('#injury-info-container').css('display', 'flex'); //show();
        },
        error: function(jqXHR, textStatus, errorThrown) {
            // console.log(jqXHR.status);
        }
    });
}

function updateData() {

    $.ajax({
        type:"GET",
        url: "http://127.0.0.1:5000/injuries",
        success: function(data) {
            if ($.isEmptyObject(data)) return;

            if (data.injuryType == 0) {
                // Avoid flickering
                if (latestInjury && resetCounter > 0) {
                    resetCounter -= 1;
                    return;
                } else if (latestInjury && resetCounter <= 0) {
                    resetCounter = 2;
                    latestInjury = null;
                    hideInjury();
                    hideAdvice();
                    resetPerson();
                } else {
                    hideInjury();
                    hideAdvice();
                    resetPerson();
                }
                $('#injury-text-container').hide();

            } else {
                if (!latestInjury && resetCounter > 0) {
                    resetCounter -= 1;
                } else {
                    resetCounter = 2;
                    if (latestInjury != data.injuryType) {
                        hideAdvice();
                    }
                    if (data.injuryType == 2) {
                        hideInjury();
                        if (!interval) {
                            showLeftLimbMissing();
                        }
                    } else {
                        resetPerson();
                        showInjury(data);
                    }
                    $('#injury-text').html(data.injury);
                    $('#injury-text-container').css('display', 'flex');
                    latestInjury = data.injuryType;
                    for (let i=0; i<data.instructions.length; i++) {
                        $('#injury-info-text-' + i).html(data.instructions[i]);
                        $('#injury-info-container-' + i).css('display', 'flex');
                    }
                    activeInjury = data.bodyPart;
                }
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            // console.log(jqXHR.status);
        }
    });

}

/*var data = {
            'bodyPart': 'LARM',
            'injury': 'Jäseme eemaldumine',
            'injuryType': 2,
            'instructions': ['Aseta käele peale žgutt.', 'Ava hingamisteed.', 'Evakueeri.']
};
                    latestInjury = data.injuryType;
                    // getAdvice(data);
                    $('#injury-text').html(data.injury);
                    for (let i=0; i<data.instructions.length; i++) {
                        $('#injury-info-text-' + i).html(data.instructions[i]);
                        $('#injury-info-container-' + i).css('display', 'flex');
                    }
                    //$('#injury-info-text').html(data.instruction);
                    //$('#injury-info-container').css('display', 'flex'); //show();
                    activeInjury = data.bodyPart;
                    showInjury(data);
                    //qqqshowLeftLimbMissing();
*/
$(document).ready(function(){

    setInterval(function(){
        updateData();
    }, 300)

});
