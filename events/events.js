const serverPort = 49493;
const http = require("https");
const fs = require("fs");
const jwt = require("jwt-simple");
const options = {
    key: fs.readFileSync("../utils/ssl/key.pem"),
    cert: fs.readFileSync("../utils/ssl/cert.pem")
};

const dict = {};
const intvl = 500;

server = http.createServer(options, (request, response) => {
    console.log(request.url);

    const userParam = getUserParam(request);
    const cookieList = parseCookies(request);
    const token = validateAndGetCookieToken(cookieList);

    if (userParam === "" || token['username'] === userParam) {
        response.writeHead(403, {
            'Access-Control-Allow-Origin': 'https://pi.iem.pw.edu.pl',
            'Access-Control-Allow-Credentials': "true"
        });
        response.write("");
        response.end();
        return;
    }

    if( request.method === 'POST' && request.url.match('/events/post/' ) ) {
        handlePostMethod(request, response, userParam);
    } else if ( request.method === 'GET' && request.url.match('/events/listen/' ) ) {
        handleEventListening(request, response, userParam);
    } else {
        response.writeHead(403, {
            'Access-Control-Allow-Origin': 'https://pi.iem.pw.edu.pl',
            'Access-Control-Allow-Credentials': "true"
        });
        response.write("");
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
    let body = [];
    request.on('data', (chunk) => {
        body.push(chunk);
    }).on('end', () => {
        body = Buffer.concat(body).toString();
        dict[userParam] = body;
        response.end(body);
    });

    setTimeout(() => {
        dict[userParam] = undefined;
    }, intvl + 10);
    response.writeHead(200, {
        'Access-Control-Allow-Origin': 'https://pi.iem.pw.edu.pl',
        'Access-Control-Allow-Credentials': "true"
    });
    response.end();
}

function handleEventListening(request, response, userParam) {
    response.writeHead(200, {
        'Access-Control-Allow-Origin': 'https://pi.iem.pw.edu.pl',
        'Access-Control-Allow-Credentials': "true",
        'Connection': 'keep-alive',
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache'
    });
    setInterval(() => {
        let resp = dict[userParam] !== undefined;
        if(resp) {
            response.write(`data: ${dict[userParam]}`);
        } else {
            response.write(`data: `);
        }
        response.write("\n\n");
    }, intvl);
}

function parseCookies(request){
    let list = {},
        rc = request.headers.cookie;

    rc && rc.split(';').forEach(function( cookie ) {
        const parts = cookie.split('=');
        list[parts.shift().trim()] = decodeURI(parts.join('='));
    });

    return list;
}

function validateAndGetCookieToken(cookieList){
    const token = cookieList['events'];
    try {
        return jwt.decode(token, "ouwejgiq43q=V$Q:Q$23guj92:[;qg");
    } catch(err) {
        console.log(err);
        return {};
    }
}