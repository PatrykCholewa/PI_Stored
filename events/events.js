const serverPort = 49493;
const http = require("https");
const fs = require("fs");
const options = {
    key: fs.readFileSync("../utils/ssl/key.pem"),
    cert: fs.readFileSync("../utils/ssl/cert.pem")
};

const dict = {};
const intvl = 500;

server = http.createServer(options, (request, response) => {
    console.log(request.url);

    const userParam = getUserParam(request);

    if (userParam === "") {
    response.writeHead(403);
    response.end();
}

    if( request.method === 'POST' && request.url.match('/events/post/' ) ) {
        handlePostMethod(request, response, userParam);
    } else if ( request.method === 'GET' && request.url.match('/events/listen/' ) ) {
        handleEventListening(request, response, userParam);
    } else {
        response.writeHead(403);
        response.end();
    }
});

server.listen(serverPort, () => {
    console.log(`SSE server started on port ` + serverPort);
});

function getUserParam(request) {
    const pathParts = request.url.split("/");
    let userParam = "";
    for( let i = 0; i < pathParts.length ; i++ ){
        if( pathParts[i] === "user" ){
            userParam = pathParts[i+1];
            break;
        }
    }
}

function handlePostMethod(request, response, userParam) {
    dict[userParam] = true;
    setTimeout(() => {
        dict[userParam] = false;
    }, intvl + 10);
    response.writeHead(200);
    response.end();
}

function handleEventListening(request, response, userParam) {
    response.writeHead(200, {
        'Access-Control-Allow-Origin': '*',
        'Connection': 'keep-alive',
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache'
    });
    setInterval(() => {
        let resp = dict[userParam] === true;
        if(resp) {
            response.write(`data: ${resp}`);
        } else {
            response.write(`data: `);
        }
        response.write("\n\n");
    }, intvl);
}