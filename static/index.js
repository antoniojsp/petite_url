// functions

function getResolution() {
     $("#response").html("Your screen resolution is: " + screen.width + "x" + screen.height);
}
function is_checkbox_checked(id){
    return $(id).prop("checked");
};

function is_url_valid(string) {
  var url;
  try {
    url = new URL(string);
  } catch (_) {
    return false;
  }
  return url.protocol === "http:" || url.protocol === "https:";
}


function hide_show_expiration(element, input) {

    var hidden_element = document.getElementById(element).style;
    if (is_checkbox_checked(input)){
        hidden_element.display = "block";
        current_time();
    } else {
        hidden_element.display = "None";
    }
};

function clear_button(){
    document.getElementById("date_local").style.display = "none";
    document.getElementById("personalized").style.display = "none";

    document.getElementById("expires_option").checked = false;
    document.getElementById("custom_hash_option").checked = false;

    document.getElementById("response").innerHTML = "";
    document.getElementById("unique_hash").innerHTML = "";

    document.getElementById("url").value = "";
    document.getElementById("custom_hash").value = "";
};

function current_time(){
    var one_minute = 60000; //to set to default  the min input  time to the current time plus one minute
    var diff_hours_to_utc = (new Date()).getTimezoneOffset() * one_minute;
    var localISOTime = (new Date(Date.now() - diff_hours_to_utc + one_minute)).toISOString().slice(0, -1);
    const dateInput = expire_time;
    dateInput.min = localISOTime.split('.')[0].slice(0, -3);
    dateInput.value = localISOTime.split('.')[0].slice(0, -3);
};

function compare_dates(input_date){
    var current_time = new Date();
    var input_time = new Date(input_date);
    return current_time.getTime() > input_time.getTime();
};

function clipboard() {
  var copyText = document.getElementById("petite_url");
    navigator.clipboard.writeText(copyText.href);
};

function is_only_alphanumeric(str) {
  return /^[A-Za-z0-9]*$/.test(str);
};

// parts of responses
var alert1 = '<div  id="response-alert" class="alert alert-success alert-dismissible fade show in text-center" role="alert">'
var alert2 = '<button class="btn btn-outline-success btn-sm" onclick="clipboard()"> </a>'
var alert3 = '</button> <button type="button" id="clear_id" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'
// Triggers
$(document).ready(function() {
    $('form').submit(function(e) {

        e.preventDefault();
        var input_url = $('#url').val();
        var information_package = {};

        if (is_url_valid(input_url) == false){
          $("#response").html(alert1 + "URL is not a valid one." + alert3);
          return
        }

        information_package['url'] = input_url
        if (is_checkbox_checked("#expires_option")){
            var input_date = document.getElementById("expire_time").value;

            if (compare_dates(input_date)){
                $("#response").html(alert1 +'The expiration date needs to be greater than the current date.' +
                alert3);
                current_time();
                return
            };

            var utc_date = new Date(input_date).toISOString();
            information_package['expiration_date'] = utc_date;
        }else{
            information_package['expiration_date'] = "None";
        };

        if (is_checkbox_checked("#custom_hash_option")){
            var partial_name = $("#custom_hash").val();

            if (is_only_alphanumeric(partial_name) == false){
                $("#response").html(alert1 + "Only alphanumeric characters (Lower or capital case)." + alert3);
                return
            }

            if (response_answer == false){
                $("#response").html(alert1 + "Personalized hash value is in use." + alert3);
                return
            };

            if (response_answer == true){
                information_package["custom_hash"] = partial_name;
                response_answer = false;
            }
        }else{
            information_package['custom_hash'] = "None";
        };


        console.log(information_package);
        clear_button();

         $.getJSON( "/_submit",
                    information_package,
                    function(data) {
                      result = data.result.response;
                      if (is_url_valid(result)){
                        $("#response").html(alert1 +'<div> The shorten URL is ' + '<a id="petite_url" href="'
                        + result + '" Target="_blank"> ' + result + '</a>' + alert2 + 'Copy!</div>' + alert3 );
                      }else{
                        $("#response").html(alert1 + result + alert3);
                      }
                    }
                 );
        });
});

var response_answer = false;
$(document).ready(function(){
    $('#custom_hash').keyup(function hash_name(){
        var partial_name = $("#custom_hash").val();
        var needs_characters = 7 - partial_name.length

        if (is_only_alphanumeric(partial_name) == false){
            $("#unique_hash").html(alert1 + "Only alphanumeric characters (Lower or capital case)." + alert3);
            return
        }else{
            $("#unique_hash").html("");
            $("#response").html("");

        };

        if (partial_name.length == 7){
            $.getJSON( "/_check_hash",
                      {name: partial_name},
                      function(data) {
                            server_response = data.result.response;
                            if (server_response){
                                $("#unique_hash").html(alert1 + "The hash is not available." + alert3);
                                response_answer = false;
                            }else{
                                $("#unique_hash").html(alert1 + "The hash is available"+ alert3);
                                response_answer = true;
                            };
                      });
        }else if(partial_name.length < 7){
             $("#unique_hash").html(alert1 + "Hash value needs to be at least 7 characters long. It needs "
                                    + needs_characters.toString() +" characters more." + alert3);
             response_answer = false;
        };
    });
});
