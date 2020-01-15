var config = require('./config.json');
var fs = require('fs');

var options = {
  cert: fs.readFileSync(config.ssl.cert),
  key: fs.readFileSync(config.ssl.key)
};

console.log('pushy');

var app = require('https').createServer(options, handler);
var redis = require('redis').createClient(config.redis.port, config.redis.host);
var io = require('socket.io')(app);
var winston = require('winston');
var debug = require('debug');

var logger = new (winston.Logger)({
	transports: [
		new (winston.transports.Console)()
		
	]
});

app.listen(config.port);

redis.psubscribe(config.pattern);

function handler (req, res) {
    return res.end('pushy');
    res.writeHead(200);
}

io.on('connection', function (socket) {
	debug('socket connection (d)')
  	console.log('socket connection');
	
	redis.on('pmessage', function(pattern, channel, data) {
		data = JSON.parse(data);
		debug('channel', channel);
		debug('data', data);

		logger.info('channel', channel);
		logger.info('data', data);

		socket.emit('push', data);
	})
	.on("error", function(err) {
        console.log("Error " + err);
    });

});
