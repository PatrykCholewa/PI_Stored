$(function(){
    get_item_list();
});

function get_item_list(){
    fetch("ws/files/list/", {
        method: "GET",
    }).then( response => response.json()
    .then(data => create_list(data)));
}

function create_list(data){
    const files = data['files'];
    let innerHtml = "";
    for( let i = 0 ; i < files.length ; i++ ){
        innerHtml = innerHtml + create_item(files[i]);
    }
    console.log(innerHtml);
    $('#panel-list').html(innerHtml);
}

function create_item(fileName){
    return '<a href="#" download onclick="get_file('
        + fileName
        + ')" class="list-group-item list-group-item-action well"><b>'
        + fileName
        + '</b></a>'
}

function get_file(filename){
    //@TODO
}