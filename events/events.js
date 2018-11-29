const serverPort = 8113;
const http = require("http");

server = http.createServer( (request, response) => {
    const pathParts = request.url.split("/");
    let userParam = "";

    for( let i = 0; i < pathParts.length ; i++ ){
        if( pathParts[i] === "user" ){
            userParam = pathParts[i+1];
            break;
        }
    }

    if (request.url.match('/events')) {
    console.log(request.headers);
    response.writeHead(200, {
        'Connection': 'keep-alive',
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache'
    });
    let lastEventId = request.headers['last-event-id'] || '1';
    let id = parseInt(lastEventId);
    setInterval(() => {
            response.write(
                `event: choice
                id: ${id}
                data: Wiadomość #${id}.
                data: Będzie więcej.`);
            response.write('\n\n');
            id++;
        }, 3000);

    } else {
        response.writeHeader(200, {"Content-Type": "text/html"});
        response.write('OK');
        response.end();
    }
});

server.listen(serverPort, () => {
    console.log(`SSE server started on port ` + serverPort);
});