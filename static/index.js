function is_box_checked(id){
    var checkBox = document.getElementById(id);
    return checkBox.checked
};

function hide_show_expiration() {
  var text = document.getElementById("date_local");

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

        console.log(input_date);
        var utc_date = new Date(input_date).toISOString();
        console.log(utc_date);

        if(is_box_checked("myCheck")){
            var package = {url: input, exp: utc_date}
        }else{
            var package = {url: input, exp: "None"}
        }

        clear_button();

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


function clear_button(){

    document.getElementById("response").innerHTML = "";
    document.getElementById("url").value = "";
    document.getElementById("exp_date").value = "2022-06-08T19:30";
    document.getElementById("myCheck").checked = false;

    if (is_box_checked("myCheck")){
    document.getElementById("date_local").style.display = "block";
    } else {
    document.getElementById("date_local").style.display = "none";
    };
}''

$("#clear").click(clear_button);






