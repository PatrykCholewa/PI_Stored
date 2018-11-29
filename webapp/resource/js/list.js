$(function(){
    set_user_param();
    get_item_list();
    listen_file_upload();
});

const event_host = "http://localhost:49493/events/";
let eventSource;
let userParam;

function get_item_list(){

    let path = "file/list";
    fetch(path, {
        method: "GET",
        headers: {
            "Accept": "application/json"
        }
    }).then( response => response.json()
    .then(data => {
        create_list(data, userParam);
    }));
}




function create_list(data){
    const files = data['files'];
    let innerHtml = "";
    for( let i = 0 ; i < files.length ; i++ ){
        const file = files[i];
        innerHtml = innerHtml + create_item(file[0], file[1], file[2]);
    }
    $('#panel-list').html(innerHtml);
    disable_adding_files_by_count(files.length);
}

function disable_adding_files_by_count(count) {
    if( count > 4 ){
        const btn = $("#add_file_btn");
        btn.attr("disabled", true);
        btn.click(function(ev){
            ev.preventDefault();
        });
    }
}

function create_item(file_id, filename, sharelink){
    let href = "../../../dl/file/" + file_id + "/name/" + filename;
    if(sharelink === undefined){
        sharelink = "";
    }
    let activeClass = sharelink === "" ? "active" : "disabled";

    return `
<div class="well">
    <div class="col-lg-12">
        <a download href="${href}" class="btn-block">
            <button type="button" class="btn btn-default btn-lg btn-block" aria-label="Left Align">
                <span class="glyphicon glyphicon-download" aria-hidden="true"></span>
                <b>${filename}</b>
            </button>
        </a> 
    </div>
    <div class="col-lg-12">
        <div class="input-group">
            <input type="text" class="form-control" placeholder="Sharelink..." readonly value="${sharelink}">
            <span class="input-group-btn">
                <button class="btn btn-default ${activeClass}" type="button" onclick="generate_sharelink('${file_id}')">
                    <span class="glyphicon glyphicon-globe" aria-hidden="true"></span>
                    Create sharelink!
                </button>
            </span>
        </div>
    </div>
</div>
`
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

function generate_sharelink(file_id){
    let path = `file/${file_id}/share`;
    fetch(path, {
        method: "POST",
    }).then( response => {
        get_item_list();
    });
}

function listen_file_upload() {
    eventSource = new EventSource(event_host + "listen/user/" + userParam);
    eventSource.addEventListener('message', (e) => {
        console.log("message: " + e.data);
        if(e.data === 'true'){
            $.notify("File uploaded");
        }
    });
}