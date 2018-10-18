const regLink = "http://edi.iem.pw.edu.pl/chaberb/register/check/";

init();

function init(){
    const login = document.getElementById("login");
    const pesel = document.getElementById("pesel");
    const password = document.getElementById("password");
    const repeat_password = document.getElementById("repeat-password");
    const myForm = document.getElementById("my-form");
    login.addEventListener("change", checkLoginAvailability, false);
    pesel.addEventListener("change", setSexByPesel, false);
    password.addEventListener("input", checkPasswordMatch, false);
    password.addEventListener("change", checkPasswordStrength, false);
    repeat_password.addEventListener("change", checkPasswordMatch, false);
    myForm.addEventListener("submit", preventFormSubmitIfNotValid, false);
}

function preventFormSubmitIfNotValid(event){
    if( !checkPasswordMatch() ){
        event.preventDefault();
        alert("Aborted submit!\nInvalid data");
    }

    const flag = checkLoginAvailabilityWithControl();

    if( flag !== true ) {
        event.preventDefault();
        alert("Login taken!");
    } else {
        alert("Success!");
    }
}

function checkLoginAvailabilityWithControl(){
    const login = document.getElementById("login").value;
    const regUrl = regLink + login;
    let ret = undefined;
    let req = new XMLHttpRequest();
    req.onreadystatechange = function() {
    if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
        const json = JSON.parse(this.responseText);
        ret = !json[login];
    }
  };
    req.open("GET", regUrl , false );
    req.send();
    return ret;
}

function checkLoginAvailability(){
    const loginInput = document.getElementById("login").value;
    const regUrl = regLink + loginInput;
    fetch(regUrl)
    .then(response => {response.json()
    .then(data => loginFreeResponseHandle(data,loginInput) )});
}

function setSexByPesel(){
    const pesel = document.getElementById("pesel").value.toString();
    if( ["1", "3", "5", "7", "9"].includes(pesel[9]) ){
        const male = document.getElementById("male");
        male.click();
    } else {
        const female = document.getElementById("female");
        female.click();
    }
}

function checkPasswordMatch(){
    const pass = document.getElementById("password").value;
    const pass2 = document.getElementById("repeat-password").value;
    let status = getStatusDiv("repeat-password-li","repeat-password-status");
    const match = pass === pass2;
    setStatus(status, match );
    return match;
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
    let div = getStatusDiv("login-li","login-status");
    const free = !json[login];
    setStatus(div, free);
    return free;
}

function getStatusDiv(liId, id) {
    let div = document.getElementById(id);

    if (div == null) {
        const loginLi = document.getElementById(liId);
        div = document.createElement('div');
        div.id = id;
        div.classList.add("input-status");
        loginLi.appendChild(div);
    }
    return div;
}

function setStatus(div, value){
    const cls = div.classList;
    if( value ){
        cls.remove("invalid-input");
        cls.add("valid-input");
        div.innerText = "OK";
    } else {
        cls.remove("valid-input");
        cls.add("invalid-input");
        div.innerText = "NOK";
    }
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