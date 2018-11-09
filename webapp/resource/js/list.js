$(function(){
    get_item_list();
});

function get_item_list(){
    fetch("cookie/user/", {
        method: "GET"
    }).then(response => response.text()
        .then( username => {
        get_item_list_by_username(username);
    }));

}

function get_item_list_by_username(username){
    let path = "../dl/user/" + username + "/list/";
    fetch(path, {
        method: "GET",
        headers: {
            "Accept": "application/json"
        }
    }).then( response => response.json()
    .then(data => {
        create_list(data, username);
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
    let href = "../dl/file/" + file_id;
    return '<a download href="'
        + href
        + '" class="list-group-item list-group-item-action well"><b>'
        + filename
        + '</b></a>'
}