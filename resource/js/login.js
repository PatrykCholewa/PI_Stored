$(function() {
    $("#login-form").submit(login);
    $("#sign-up").click(redirectToRegister);
});

function login() {

}

function redirectToRegister() {
    window.location = "register";
}
