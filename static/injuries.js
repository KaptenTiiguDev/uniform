var limbMissing = false;
var interval = null;
var limbVisualIndex = false;
function hideInjury() {
    $('.body-spot').hide();
}

function hideAdvice() {
    $('#injury-info-text').html('');
    $('#injury-info-container').hide();
}

function showInjury(data) {
    $('#body-spot-' + data.no).show();
}

function showLeftLimbMissing() {
    interval = setInterval(function() {
        limbVisualIndex = !limbVisualIndex;
        var imgUrl = !limbVisualIndex ? "../static/body2.png" : "../static/body_nohand.png";
        $("#body-figure").attr("src",imgUrl);
    }, 400);
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
        type:"POST",
        url: "http://localhost:5000/injuries",
        success: function(data) {

            if ($.isEmptyObject(data)) {
                hideInjury();
                hideAdvice();
                resetPerson();
            } else {
                if (data.inj == 2) {
                    hideInjury();
                    if (!interval) {
                        showLeftLimbMissing();
                    }
                } else {
                    resetPerson();
                    showInjury(data);
                }
                // getAdvice(data);
                $('#injury-info-text').html(data.advice);
                $('#injury-info-container').css('display', 'flex'); //show();
                activeInjury = data.no;
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            // console.log(jqXHR.status);
        }
    });

}

$(document).ready(function(){

    setInterval(function(){
        updateData();
    }, 200)

});
