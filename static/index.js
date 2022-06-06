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
});


function myFunction() {
  // Get the checkbox
  var checkBox = document.getElementById("myCheck");
  // Get the output text
  var text = document.getElementById("text");

  // If the checkbox is checked, display the output text
  if (checkBox.checked == true){
    text.style.display = "block";
  } else {
    text.style.display = "none";
  }
}
