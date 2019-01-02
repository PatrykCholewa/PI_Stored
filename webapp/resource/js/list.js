$(function(){
    set_user_param();
});

function generate_sharelink(file_id){
    let path = `file/${file_id}/share`;
    fetch(path, {
        method: "POST",
    }).then( response => {
        location.reload(true);
    });
}