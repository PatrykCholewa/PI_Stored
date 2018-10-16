const regLink = "http://edi.iem.pw.edu.pl/chaberb/register/check/";

init();

function init(){
    const login = document.getElementById("login");
    const pesel = document.getElementById("pesel");
    const password = document.getElementById("password");
    const repeat_password = document.getElementById("repeat-password");
    login.addEventListener("change", checkLoginAvailability, false);
    pesel.addEventListener("change", setSexByPesel, false);
    password.addEventListener("change", checkPasswordMatch, false);
    repeat_password.addEventListener("change", checkPasswordMatch, false);
}

function checkLoginAvailability(){
    const loginInput = document.getElementById("login").value;
    const regUrl = regLink + loginInput;
    const ret = fetch(regUrl)
    .then(response => {response.json()
    .then(data => loginFreeResponseHandle(data,loginInput) )});
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

function loginFreeResponseHandle(data,login){
    let json = data;
    let div = document.getElementById("login-status");

    if( div == null ){
        createNewLoginStatus();
        div = document.getElementById("login-status");
    }

    const cls = div.classList;

    if( json[login] ){
        cls.remove("valid-input");
        cls.add("invalid-input");
        div.innerText = "NOK";
    } else {
        cls.remove("invalid-input");
        cls.add("valid-input");
        div.innerText = "OK";
    }

}

function createNewLoginStatus(){
    const loginLi = document.getElementById("login-li");
    let div = document.createElement('div');

    div.id = "login-status";
    div.classList.add("input-status");
    loginLi.appendChild(div);
}