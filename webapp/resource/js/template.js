$(function(){
    $('#header').load('template/header.html');
});

function logout(){
    fetch("ws/logout/", {
        method: "POST"
    }).then( response => {
        window.location = "login";
    });
    return false;
}