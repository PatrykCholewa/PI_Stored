$(function(){
    $("#login-form").submit(login);
    $("#sign-up").click(redirectToRegister);
});

function login(event) {
    event.preventDefault();
    fetch("ws/login/", {
        method: "POST",
        body: "user-id:cholewp1\npassword=pass"
    }).then( response => {
        if (response.statusCode === 200) {
            window.location = "list";
        } else {
            console.log(response);
        }
    });
    return false;
}

function redirectToRegister() {
    window.location = "register";
}
