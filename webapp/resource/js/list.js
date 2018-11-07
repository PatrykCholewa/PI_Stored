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
    let path = "../dl/" + username + "/list/";
    fetch(path, {
        method: "GET",
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

function create_list(data, username){
    const files = data['files'];
    let innerHtml = "";
    for( let i = 0 ; i < files.length ; i++ ){
        innerHtml = innerHtml + create_item(files[i], username);
    }
    $('#panel-list').html(innerHtml);
}

function create_item(fileName, username){
    let href = "../dl/" + username + /file/ + fileName;
    return '<a download href="'
        + href
        + '" class="list-group-item list-group-item-action well"><b>'
        + fileName
        + '</b></a>'
}