console.log("Server ")

var PORT = 12344;
var HOST = '127.0.0.1';

var dgram = require('dgram');
console.log("check1")
var server = dgram.createSocket('udp4');

console.log("check2")

server.on('listening', function() {
  
  console.log("check3")
  var address = server.address();
 console.log('UDP Server listening on ' + address.address + ':' + address.port);
});

server.on('message', function(message, remote) {
 console.log(remote.address + ':' + remote.port +' - ' + message);
});

server.bind(PORT, HOST);