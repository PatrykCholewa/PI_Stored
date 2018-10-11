// http://edi.iem.pw.edu.pl/chaberb/register/check/

init();

function init(){
    const login = document.getElementById("login");
    const pesel = document.getElementById("pesel");
    const password = document.getElementById("password");
    const repeat_password = docuemnt.getElementById("repeat-password");
    login.addEventListener("change", check_login_availability, false);
    pesel.addEventListener("change", setSexByPesel, false);
    password.addEventListener("change", checkPasswordMatch, false);
    repeat_password.addEventListener("change", checkPasswordMatch, false);
}

function check_login_availability(){
    @TODO
    const login = document.getElementById("login");
    login.classList.add("invalid-input");
}

function setSexByPesel(){
    @TODO
}

function checkPasswordMatch(){
    @TODO
}