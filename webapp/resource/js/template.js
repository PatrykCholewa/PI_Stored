$(function(){
    $('#header').load('/cholewp1/webapp/template/header.html');
    set_user_param();
    listen_file_upload();
});

const event_host = "https://pi.iem.pw.edu.pl:49493/events/";
let eventSource;
let userParam = "";

function logout(){
    fetch("/cholewp1/webapp/ws/logout/", {
        method: "POST"
    }).then( response => {
        window.location = "/cholewp1/webapp/";
    });
    return false;
}

function listen_file_upload() {
    if(userParam === ""){
        return;
    }

    eventSource = new EventSource(event_host + "listen/user/" + userParam);
    eventSource.addEventListener('message', (e) => {
        if(e.data !== ''){
            if( !window.location.pathname.endsWith("list")){
                window.location.pathname = window.location.pathname + '/../list';
            }
            $.notify(`File \"${e.data}\" uploaded. Please, refresh.`,
                {
                    className: "success",
                    autoHide: false,
                    globalPosition: 'bottom right'
                });
        }
    });
}

function set_user_param(){
    const windowPath = window.location.pathname;
    const pathParts = windowPath.split("/");

    for( let i = 0; i < pathParts.length ; i++ ){
        if( pathParts[i] === "user" ){
            userParam = pathParts[i+1];
            break;
        }
    }
}