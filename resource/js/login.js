$(function() {
    $("#login-form").submit(login);
    $("#sign-up").click(redirectToRegister);
});

function login(event) {
    event.preventDefault();
    console.log("OK");
    fetch("ws/login/", {
        method: "POST",
        form: event.form
    }).then( response => {
        if (response.statusCode === 200) {
            window.location = "list";
        } else {
            console.log("NOK");
        }
    });
    return false;
}

function redirectToRegister() {
    window.location = "register";
}
