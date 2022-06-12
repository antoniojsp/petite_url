// functions
function is_checkbox_checked(id){
    var checkBox = document.getElementById(id);
    return checkBox.checked
};

function hide_show_expiration(element, input) {
  var text = document.getElementById(element);

  if (is_checkbox_checked(input)){
    text.style.display = "block";
    current_time();
  } else {
    text.style.display = "None";
  }
};

function clear_button(){
    // compatible if expiration is checked or not
    var text = document.getElementById("date_local");
    // catch cases if the expiration block is showing or not
    if (text.style.display == "block"){
        text.style.display = "none";
    }

    var text = document.getElementById("personalized");
    if (text.style.display == "block"){
        text.style.display = "none";
    }

    document.getElementById("expires").checked = false;
    document.getElementById("personalized_name").checked = false;

    document.getElementById("response").innerHTML = "";
    document.getElementById("unique_hash").innerHTML = "";

    document.getElementById("url").value = "";
    document.getElementById("per_name").value = "";

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
  var copyText = document.getElementById("petite_url");
  console.log(copyText.href);
  navigator.clipboard.writeText(copyText.href);
};

// Triggers
$(document).ready(function() {
    $('form').submit(function(e) {
        e.preventDefault();
        var input_url = document.getElementById("url").value;
        var information_package = {};

        information_package['url'] = input_url

        // response alerts parts
        var alert1 = '<div id="response-alert" class="alert alert-success alert-dismissible fade show" role="alert">'
        var alert2 = '<button class="btn btn-outline-success btn-sm" onclick="clipboard()"> </a>'
        var alert3 = '</button> <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'

        if (is_checkbox_checked("expires")){
            var input_date = document.getElementById("exp_date").value;

            if (compare_dates(input_date)){
                $("#response").html(alert1 +
                'The expiration date needs to be greater than the current date.' +
                alert3);
                current_time();
                return
            };
            var utc_date = new Date(input_date).toISOString();
            information_package['expiration_date'] = utc_date;
        }else{
            information_package['expiration_date'] = "None";
        };

        if (is_checkbox_checked("personalized_name")){
            console.log("expires")
            var partial_name = $("#per_name").val();

           if(partial_name.length != 7){
                $("#response").html("Personalised hash needs to be 7 character long");
                return
            }
            if (response_answer == false){
                $("#response").html("Hash in use.");
                return
            };

            if (partial_name.length != 7 ||  response_answer == false){
                console.log(response_answer);
                console.log(partial_name);
                return
            }else if (partial_name.length == 7 && response_answer == true){
                information_package["per_name"] = partial_name;
                response_answer = false;
            }
        }else{
            information_package['per_name'] = "None";
        };


        console.log(information_package);
        clear_button();

         $.getJSON( "/_submit",
                    information_package,
                    function(data) {
                      result = data.result.response;
                      is_href_link = data.result.href;
                      if (is_href_link == true){
                        $("#response").html(alert1 +' The shorten URL is ' + '<a id="petite_url" href=" '
                        + result + '  "Target="_blank">' + result + '</a>   '+ alert2 +
                         '   Copy PetiteURL!' + alert3 );
                      }else{
                      $("#response").html(alert1 + result + alert3);
                      }
                    }
                 );
        });
});




var response_answer = false;
$(document).ready(function(){
    $('#per_name').keyup(function hash_name(){
    var partial_name = $("#per_name").val();
    if (partial_name.length == 7){
        $.getJSON( "/_check_name",
                  {name: partial_name},
                  function(data) {
                        response_answer = data.result.response;
                        rsval = data.result.response;
                        if (rsval){
                            $("#unique_hash").html("Existe");
                            response_answer = false;
                        }else{
                            $("#unique_hash").html("No existe");
                            response_answer = true;
                        };
                  });
    }else if(partial_name.length > 7){
         $("#unique_hash").html("7 character max");
         response_answer = false;
    }else if(partial_name.length < 7){
         $("#unique_hash").html("");
         response_answer = false;
    };
});
});
