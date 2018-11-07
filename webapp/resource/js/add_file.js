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

    fetch("cookie/user/", {
        method: "GET"
    }).then( response => response.text()
    .then(username => {
        let path = "../dl/" + username + "/add/";
        act_sending_file(file, path);
    }));
}

function act_sending_file(file, path){
    let data = new FormData();
    data.append('file', file);

    fetch(path, {
        method: "POST",
        body: data
    })
    .then(response => {
        if( response.ok ){
            window.location = "list";
        } else {
            console.log(response);
            alert("Failed!");
        }
    });
}