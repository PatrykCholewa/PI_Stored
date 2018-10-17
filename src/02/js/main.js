const regLink = "http://edi.iem.pw.edu.pl/chaberb/register/check/";

init();

function init(){
    const login = document.getElementById("login");
    const pesel = document.getElementById("pesel");
    const password = document.getElementById("password");
    const repeat_password = document.getElementById("repeat-password");
    login.addEventListener("change", checkLoginAvailability, false);
    pesel.addEventListener("change", setSexByPesel, false);
    password.addEventListener("key-up", checkPasswordStrength, false);
    password.addEventListener("change", checkPasswordMatch, false);
    password.addEventListener("change", checkPasswordStrength, false);
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
    let meter = document.getElementById("password-meter");
    const password = document.getElementById("password").value;

    if( meter == null ){
        meter = createNewPasswordMeter();
    }

    meter.value = 0;
    if( /\d/.test(password) ){
        meter.value = meter.value + 0.25;
    }
    if( password.length > 7 ){
        meter.value = meter.value + 0.25;
    }
    if( /[a-z]/.test(password) ){
        meter.value = meter.value + 0.25;
    }
    if( /[A-Z]/.test(password) ){
        meter.value = meter.value + 0.25;
    }
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

function createNewPasswordMeter(){
    const passwordLi = document.getElementById("password-li");
    let meter = document.createElement("meter");

    meter.id = "password-meter";
    meter.low = 0.3;
    meter.high = 0.8;
    meter.optimum = 0.9;
    passwordLi.appendChild(meter);
    return meter;
}