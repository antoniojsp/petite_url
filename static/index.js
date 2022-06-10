function is_expiration_checked(id){
    var checkBox = document.getElementById(id);
    return checkBox.checked
};

function hide_show_expiration() {
  var text = document.getElementById("date_local");

  if (is_expiration_checked("myCheck")){
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



        if(is_expiration_checked("myCheck")){
            var input_date = document.getElementById("exp_date").value;

            if (compare_dates(input_date)){
                console.log("aaaa")
                $("#response").html("The expiration date needs to be greater than the current date." );
                current_time();
                return
            };

            var utc_date = new Date(input_date).toISOString();
            var package = {url: input_url, expiration_date: utc_date}
        }else{
            var package = {url: input_url, expiration_date: "None"}
        };

        clear_button();

         $.getJSON( "/_submit",
                    package,
                    function(data) {
                      result = data.result.response;
                      is_href_link = data.result.href;
                      if (is_href_link == true){
                      $("#response").html("The shorten URL is " + "<a id='petite_url' href='" + result +
                      "' Target='_blank'>" + result + "</a>" + "  <button class='btn btn-outline-success btn-sm' onclick='clipboard()'> Copy PetiteURL!</button>" );
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

    // catch cases if the expiration block is showing or not
    if (text.style.display == "block"){
        text.style.display = "none";
    }

    document.getElementById("myCheck").checked = false;
    document.getElementById("response").innerHTML = "";
    document.getElementById("url").value = "";


};

function current_time(){
    var one_minute = 60000;
    var diff_hours_to_utc = (new Date()).getTimezoneOffset() * 60000;
    var localISOTime = (new Date(Date.now() - diff_hours_to_utc + one_minute)).toISOString().slice(0, -1);
    const dateInput = exp_date;
    dateInput.min = localISOTime.split('.')[0].slice(0, -3);
    dateInput.value = localISOTime.split('.')[0].slice(0, -3);
};

function compare_dates(input_date){
    var current_time = new Date();
    var input_time = new Date(input_date);
    return current_time.getTime() > input_time.getTime();
};

function clipboard() {
  /* Get the text field */
  var copyText = document.getElementById("petite_url");
  console.log(copyText.href);
  navigator.clipboard.writeText(copyText.href);
};