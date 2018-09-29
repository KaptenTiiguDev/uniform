$(document).ready(function()
{
    $SCRIPT_ROOT = '';

    $( "body" ).find( ".questionAnswer" ).click(

        function()
        {
            console.log("Hey");
            var x ={ "name":"John", "age":30, "car":null }
            sendDataToBackend(x);
            return false;
        });

    function sendDataToBackend(x) {
        $.post( $SCRIPT_ROOT, {
            data: x
        });
    }



});



