$(function(){
    set_user_param();
});

let userParam = "";

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