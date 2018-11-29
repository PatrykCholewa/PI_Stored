const serverPort = 49493;
const http = require("http");

const dict = {};

server = http.createServer( (request, response) => {
    const pathParts = request.url.split("/");
    let userParam = "";

    for( let i = 0; i < pathParts.length ; i++ ){
        if( pathParts[i] === "user" ){
            userParam = pathParts[i+1];
            break;
        }
    }
    if( userParam === "" ){
        response.writeHead(403);
        response.end();
    } else if (request.url.match('/events/listen/')) {
        response.writeHead(200, {
            'Connection': 'keep-alive',
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache'
        });
        setInterval(() => {
            let resp = dict[userParam] === true;
            response.write(`event: ${resp}`);
            response.write("\n\n");
            if( resp === true ){
                setTimeout(() => dict[userParam] = false, 3000);
            }
        }, 1000);

    } else if(request.url.match('/events/post/')) {
        dict[userParam] = true;
        response.writeHead(200);
        response.write("OK");
        response.end();
    } else {
        response.writeHead(400);
        response.end();
    }
});

server.listen(serverPort, () => {
    console.log(`SSE server started on port ` + serverPort);
});