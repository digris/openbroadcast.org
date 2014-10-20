
var config = require('./config.json');
var io = require('socket.io').listen(config.port);
var redis = require('redis').createClient(config.redis.port, config.redis.host);
var winston = require('winston');
var debug = require('debug')('pushy');

var logger = new (winston.Logger)({
	transports: [
		new (winston.transports.Console)(),
		//new (winston.transports.File)({
		//	filename: 'pushy.log'
		//})
	]
});


redis.psubscribe(config.pattern);


io.sockets.on('connection', function (socket) {

	debug('socket connection')
	
	logger.info('socket connection');

	redis
	.on('pmessage', function(pattern, channel, data) {
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

