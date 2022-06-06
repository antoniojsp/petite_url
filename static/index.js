function is_box_checked(id){
    var checkBox = document.getElementById(id);
    return checkBox.checked
};


function myFunction() {
  var text = document.getElementById("text");

  if (is_box_checked("myCheck")){
    text.style.display = "block";
  } else {
    text.style.display = "none";
  }
};

$(document).ready(function() {
    $('form').submit(function(e) {
        e.preventDefault();
        var input = document.getElementById("url").value;
        var input_date = document.getElementById("exp_date").value;
        document.getElementById("url").value = "";

        if(is_box_checked("myCheck")){
            var package = {url: input, exp: input_date}
        }else{
            var package = {url: input, exp: "None"}
        }

    console.log(package)
     $.getJSON( "/_submit",
                package,
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




