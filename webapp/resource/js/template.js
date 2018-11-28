$(function(){
    $('#header').load('/cholewp1/webapp/template/header.html');
});

function logout(){
    fetch("/cholewp1/webapp/ws/logout/", {
        method: "POST"
    }).then( response => {
        window.location = "login";
    });
    return false;
}