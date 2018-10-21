$(function(){
    get_item_list();
});

function get_item_list(){
    fetch("ws/files/list/", {
        method: "GET",
    }).then( response => {
        if (response.ok) {
            console.log("OK");
            console.log(response);
        } else {
            console.log("NOK");
            console.log(response);
        }
    });
}

function create_item(){

}