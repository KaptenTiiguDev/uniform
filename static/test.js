$(document).ready(function()
{
    $SCRIPT_ROOT = 'http://localhost:5000/getAnswer/';

    $( "body" ).find( ".questionAnswer" ).click(

        function()
        {
            console.log("Hey");
            var x ="test"
            sendDataToBackend(x);
            return false;
        });

    function sendDataToBackend(x) {
        console.log(x)
        $.post( $SCRIPT_ROOT+x, {
            data: x
        });
    }



});



