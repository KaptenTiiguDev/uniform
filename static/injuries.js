
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

            } else {
                if (data.no != activeInjury) {
                    showInjury(data);
                    getAdvice(data);
                    activeInjury = data.no;
                }
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            // console.log(jqXHR.status);
        }
    });

}

var activeInjury = null;

$(document).ready(function(){

    setInterval(function(){
        updateData();
    }, 1000)

});
