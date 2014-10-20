var io = require('socket.io').listen(8888);
var redis = require('redis').createClient();

redis.psubscribe('push_*');

io.sockets.on('connection', function (socket) {
	
	console.log('io.sockets.on connection');
	
	redis.on('pmessage', function(pattern, channel, data){
		
		data = JSON.parse(data);
		
		// console.log(channel, data);		
		console.log('i-pattern:', pattern);
		console.log('i-route:', data.route);
		
		socket.emit('push', data);

	})
	
});

