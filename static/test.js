$(document).ready(function()
{
    $SCRIPT_ROOT = '';

    $( "body" ).find( ".questionAnswer" ).click(

        function()
        {
            console.log("Hey");
            var x ="test"
            sendDataToBackend(x);
            return false;
        });

    function sendDataToBackend(x) {
        $.post( $SCRIPT_ROOT, {
            data: x
        });
    }



});



