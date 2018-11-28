$(function(){
    get_item_list();
});

function get_item_list(){

    const windowPath = window.location.pathname;
    const pathParts = windowPath.split("/");
    let userParam = "";

    for( let i = 0; i < pathParts.length ; i++ ){
        if( pathParts[i] === "user" ){
            userParam = pathParts[i+1];
            break;
        }
    }

    let path = "file/list";
    fetch(path, {
        method: "GET",
        headers: {
            "Accept": "application/json"
        }
    }).then( response => response.json()
    .then(data => {
        create_list(data, userParam);
        check_item_count();
    }));
}


function check_item_count() {
    const items = $(".list-group-item");
    if( items.length > 4 ){
        const btn = $("#add_file_btn")
        btn.attr("disabled", true);
        btn.click(function(ev){
            ev.preventDefault();
        });
    }
}

function create_list(data){
    const files = data['files'];
    let innerHtml = "";
    for( let i = 0 ; i < files.length ; i++ ){
        const file = files[i];
        innerHtml = innerHtml + create_item(file[0], file[1]);
    }
    $('#panel-list').html(innerHtml);
}

function create_item(file_id, filename){
    let href = "../../../dl/file/" + file_id + "/name/" + filename;
    return '<a download href="'
        + href
        + '" class="list-group-item list-group-item-action well"><b>'
        + filename
        + '</b></a>'
}