$(function(){
    $("#login-form").submit(login);
    $("#sign-up").click(redirectToRegister);
});

function login(event) {
    event.preventDefault();

   let data = new FormData(document.getElementById("login-form"));

    fetch("ws/login/", {
        method: "POST",
        body: data
    }).then( response => {
        if (response.ok) {
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
