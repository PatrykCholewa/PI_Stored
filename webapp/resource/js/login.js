$(function(){
    $("#login-form").submit(login);
    // $("#sign-up").click(redirectToRegister);
    $("#sign-up").click(function(){alert("Not implemented yet!")});
});

function login(event) {
    event.preventDefault();

   let data = new FormData(document.getElementById("login-form"));

    fetch("webapp/login/", {
        method: "POST",
        body: data
    }).then( response => {
        if (response.ok) {
            window.location = "list";
        } else {
            $("#login-panel").addClass("panel-danger");
            $("#login-panel-heading").text("Invalid user ID or password!");
        }
    });
    return false;
}

function redirectToRegister() {
    window.location = "register";
}
