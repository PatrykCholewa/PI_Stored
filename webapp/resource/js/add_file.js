$(function(){
    const dropZone = $("#drop-zone");
    dropZone.on("drop", handle_file_drop);
    dropZone.on("dragenter", function(){
        dropZone.addClass("drop");
        event.preventDefault();
        event.stopPropagation();
    });
    dropZone.on("dragleave", function(){
        dropZone.removeClass("drop");
        event.preventDefault();
        event.stopPropagation();
    });
    dropZone.on("dragover", function(){
        event.preventDefault();
        event.stopPropagation();
    })
});

function handle_file_drop(event){
    event.preventDefault();
    event.stopPropagation();
    $("#drop-zone").removeClass("drop");

    const dt = event.originalEvent.dataTransfer;
    if(dt.files.length > 0) {
        return send_file(dt.files[0]);
    }

    return null;

}

function send_file(file){

    const path = window.location.pathname;
    const pathParts = path.split("/");
    let userParam = "";

    for( let i = 0; i < pathParts.length; i++ ){
        if( pathParts[i] === "user" ){
            userParam = pathParts[i+1];
            break;
        }
    }

    let data = new FormData();
    data.append('file', file);

    fetch("file/add", {
        method: "POST",
        body: data
    }).then( response => response.json()
    .then(data => {
        let path = "../../../dl/file/" + data['file_id'];
        act_sending_file(file, path, data);
    }));
}

function act_sending_file(file, path, fileJson){
    let data = new FormData();
    data.append('file', file);

    fetch(path, {
        method: "POST",
        body: data
    })
    .then(response => {
        if( response.ok ){
            confirm_sending_file(fileJson)
        } else {
            console.log(response);
            alert("Failed!");
        }
    });
}

function confirm_sending_file(fileJson){
    fetch("file/"+fileJson['file_id']+"/confirm/"+fileJson['filename'], {
        method: "POST",
    })
    .then(response => {
        if( response.ok ){
            notify_file_uploaded(fileJson['filename']);
        } else {
            console.log(response);
            alert("Failed!");
        }
    });
}

function notify_file_uploaded(filename){
    fetch("events/cookie", {
        method: "GET",
        credentials: 'include'
    }).then( response => {
        fetch(event_host + "post/user/" + userParam, {
            method: "POST",
            body: filename
        }).then(response => {
            window.location = "list";
        });
    });
}