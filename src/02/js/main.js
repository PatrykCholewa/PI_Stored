// http://edi.iem.pw.edu.pl/chaberb/register/check/

init();

function init(){
    const login = document.getElementById("login");
    const pesel = document.getElementById("pesel");
    const password = document.getElementById("password");
    const repeat_password = document.getElementById("repeat-password");
    login.addEventListener("change", check_login_availability, false);
    pesel.addEventListener("change", setSexByPesel, false);
    password.addEventListener("change", checkPasswordMatch, false);
    repeat_password.addEventListener("change", checkPasswordMatch, false);
}

function check_login_availability(){
    //@TODO
    const loginLi = document.getElementById("login-li");
    let div = document.getElementById("login-status");

    if( div == null ){
        div = document.createElement( 'div' );
        div.innerText = "OK";
        div.id = "login-status";
        const clsList = div.classList;
        clsList.add("valid-input");
        clsList.add("input-status");
        loginLi.appendChild(div);
    }



}

function setSexByPesel(){
    //@TODO
}

function checkPasswordMatch(){
    //@TODO
}

function checkPasswordStrength(){
    //@TODO
}