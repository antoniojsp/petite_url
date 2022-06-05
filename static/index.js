$(document).ready(function() {
    $('form').submit(function(e) {
        e.preventDefault();
        var input = document.getElementById("url").value;
        document.getElementById("url").value = "";

     $.getJSON( "/_submit",
                {url: input},
                function(data) {
                  result = data.result.response;
                  is_href_link = data.result.href;
                  if (is_href_link == true){
                  $("#response").html("The shorten URL is " + "<a href='" + result + "' Target='_blank'>" + result + "</a>" );
                  }else{
                  $("#response").html(result);
                  }
                }
             );
    });
});

$("#clear").click(function(){
    document.getElementById("response").innerHTML = "";
})
