function errorLoginMsg(message) {
    $("#login-info").removeClass('alert alert-success');
    $("#login-info").addClass("alert alert-danger").html(message);
}

function successLoginMsg(message) {
    $("#login-info").removeClass('alert alert-danger');
    $("#login-info").addClass("alert alert-success").html(message);
}

$(function(){
    var inputusername = $("input[type=text]");
    var inputpassward = $("input[type=password]");
    $('button[type="submit"]').click(function(e1) {
        e1.preventDefault();
        if (inputusername.val() != "" && inputpassward.val() != "") {
            //@@ add feature later: save username+password in MySQL
            if (inputusername.val() == "open" && inputpassward.val() == "sesame") {
                successLoginMsg("Welcom");

                // change button from "login" to "continue", and reset the input boxes
                $('button[type="submit"]')
                    .html("continue")
                    .removeClass("btn-info")
                    .addClass("btn-success").click(function(e2){
                        e2.preventDefault();
                        // clear input boxes after a successful login
                        $("input").val("");
                        // @@ to tabularresults, do this later 
                    });
            } else if (inputusername.val() == "open" && inputpassward.val() != "sesame") {
                //@@ modify this later: check if inputusername.val() in DB
                errorLoginMsg("wrong passward");
            } else {
                errorLoginMsg("wrong username or passward"); //@@ add feature later
            } 
        } else if (inputusername.val() != "") {
            errorLoginMsg("please enter your passward")
        } else if (inputpassward.val() != "") {
            errorLoginMsg("please enter your username")
        } else {
            errorLoginMsg("please enter username and passward")
        }
    });
});
