function is_box_checked(id){
    var checkBox = document.getElementById(id);
    return checkBox.checked
};

function hide_show_expiration() {
  var text = document.getElementById("date_local");

  if (is_box_checked("myCheck")){
    text.style.display = "block";
    current_time();
  } else {
    text.style.display = "None";
  }
};

$(document).ready(function() {
    $('form').submit(function(e) {
        e.preventDefault();
        var input_url = document.getElementById("url").value;
        // if expiration is checked.
        var input_date = document.getElementById("exp_date").value;
        console.log(input_date);
        var utc_date = new Date(input_date).toISOString();

        if(is_box_checked("myCheck")){
            var package = {url: input_url, exp: utc_date}
        }else{
            var package = {url: input_url, exp: "None"}
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
    // compatible if expiration is checked or not
    var text = document.getElementById("date_local");

    if (text.style.display == "block"){
        text.style.display = "none";
    }

    document.getElementById("myCheck").checked = false;
    document.getElementById("response").innerHTML = "";
    document.getElementById("url").value = "";


};

function current_time(){
    var diff_hours_to_utc = (new Date()).getTimezoneOffset() * 60000;
    var localISOTime = (new Date(Date.now() - diff_hours_to_utc + 60000)).toISOString().slice(0, -1);
    const dateInput = exp_date;
    dateInput.min = localISOTime.split('.')[0].slice(0, -3);
    dateInput.value = localISOTime.split('.')[0].slice(0, -3);
};