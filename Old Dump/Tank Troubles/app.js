var app = require('http').createServer(handler)
  , io = require('/home/ydhamija96/other_software/node_modules/socket.io').listen(app)
  , fs = require('fs')
app.listen(8080);
function handler (req, res) {
  fs.readFile(__dirname + '/index.html',
  function (err, data) {
    if (err) {
      res.writeHead(500);
      return res.end('Error loading index.html');
    }
    res.writeHead(200);
    res.end(data);
  });
}
function toDegrees (angle) {
	return angle * (180 / Math.PI);
} 
function toRadians (angle) {	
	return angle * (Math.PI / 180);
} 
var left = 60;	
var top = 60;	
var angle = 0;	
var left2 = 500; 
var top2 = 500;	
var angle2 = 180;  
var moveSpeed = 7;  
var turnSpeed = 1.5*moveSpeed;  
var bulletSpeed = 1.1*moveSpeed; 
var backwardsSpeed = 0.6;  
var shot1 = 0;
var shot2 = 0;
var bulletTop1;
var bulletLeft1;
var bulletAngle1;
var bulletTop2;
var bulletLeft2;
var bulletAngle2;
var leftflip1 = 0;
var topflip1 = 0;
var leftflip2 = 0;
var topflip2 = 0;
var bullet1interval;
var bullet2interval;
var hiddenbullet1 = 1;
var hiddenbullet2 = 1;
io.sockets.on('connection', function (socket) {
	io.sockets.emit('position', {left:left, top:top, angle:angle});  
	io.sockets.emit('position2', {left:left2, top:top2, angle:angle2}); 
	socket.on('up', function(data){ 
		left = left + (Math.cos(toRadians(angle)) * moveSpeed); 
		top = top + (Math.sin(toRadians(angle)) * moveSpeed);
		io.sockets.emit('position', {left:left, top:top, angle:angle});
		
	});
	socket.on('down', function(data){  
		left = left - (Math.cos(toRadians(angle)) * backwardsSpeed * moveSpeed); 
		top = top - (Math.sin(toRadians(angle)) * backwardsSpeed * moveSpeed);  
		io.sockets.emit('position', {left:left, top:top, angle:angle});  
	});
	socket.on('left', function(data){ 
		angle = angle - turnSpeed;  
		if(angle>=360 || angle<=-360){
			angle=0;
		}
		io.sockets.emit('position', {left:left, top:top, angle:angle}); 		
	});
	socket.on('right', function(data){ 
		angle = angle + turnSpeed; 
		if(angle>=360 || angle<=-360){ 
			angle=0;
		}
		io.sockets.emit('position', {left:left, top:top, angle:angle}); 
	});
	socket.on('upw', function(data){
		left2 = left2 + (Math.cos(toRadians(angle2)) * moveSpeed);
		top2 = top2 + (Math.sin(toRadians(angle2)) * moveSpeed);
		io.sockets.emit('position2', {left:left2, top:top2, angle:angle2});
	});
	socket.on('downs', function(data){
		left2 = left2 - (Math.cos(toRadians(angle2)) * backwardsSpeed * moveSpeed);
		top2 = top2 - (Math.sin(toRadians(angle2)) * backwardsSpeed * moveSpeed);
		io.sockets.emit('position2', {left:left2, top:top2, angle:angle2});
	});
	socket.on('lefta', function(data){
		angle2 = angle2 - turnSpeed;
		if(angle2>=360 || angle2<=-360){
			angle2=0;
		}
		io.sockets.emit('position2', {left:left2, top:top2, angle:angle2});
	});
	socket.on('rightd', function(data){
		angle2 = angle2 + turnSpeed;
		if(angle2>=360 || angle2<=-360){
			angle2=0;
		}
		io.sockets.emit('position2', {left:left2, top:top2, angle:angle2});
	});
	socket.on('fire1', function(data){
		if(shot1==0){
			hiddenbullet1 = 0;
			leftflip1 = 0;
			topflip1 = 0;
			bulletTop1 = top;
			bulletLeft1 = left;
			bulletAngle1 = angle;
			bulletLeft1 = bulletLeft1 + (Math.cos(toRadians(bulletAngle1)) * 35);
			bulletTop1 = bulletTop1 + (Math.sin(toRadians(bulletAngle1)) * 35);
			io.sockets.emit('bullet1loc', {left:bulletLeft1, top:bulletTop1, angle:bulletAngle1});
			shot1 = 1;
			bullet1interval = setInterval(function(){
				if(leftflip1==0){
					bulletLeft1 = bulletLeft1 + (Math.cos(toRadians(bulletAngle1)) * bulletSpeed);
				}
				else{
					bulletLeft1 = bulletLeft1 - (Math.cos(toRadians(bulletAngle1)) * bulletSpeed);
				}
				if(topflip1==0){
					bulletTop1 = bulletTop1 + (Math.sin(toRadians(bulletAngle1)) * bulletSpeed);
				}
				else{
					bulletTop1 = bulletTop1 - (Math.sin(toRadians(bulletAngle1)) * bulletSpeed);
				}
				io.sockets.emit('bullet1loc', {left:bulletLeft1, top:bulletTop1, angle:bulletAngle1});
			}, 25);
			setTimeout(function(){
				clearInterval(bullet1interval);
				bullet1interval = 0;
				shot1 = 0;
				if(hiddenbullet1==0){
					io.sockets.emit('bullet1hide');
					hiddenbullet1=1;
				}
			}, 12000);
		}
	});
	socket.on('fire2', function(data){
		if(shot2==0){
			hiddenbullet2 = 0;
			leftflip2 = 0;
			topflip2 = 0;
			bulletTop2 = top2;
			bulletLeft2 = left2;
			bulletAngle2 = angle2;
			bulletLeft2 = bulletLeft2 + (Math.cos(toRadians(bulletAngle2)) * 35);
			bulletTop2 = bulletTop2 + (Math.sin(toRadians(bulletAngle2)) * 35);
			io.sockets.emit('bullet2loc', {left:bulletLeft2, top:bulletTop2, angle:bulletAngle2});
			shot2 = 1;
			bullet2interval = setInterval(function(){
				if(leftflip2==0){
					bulletLeft2 = bulletLeft2 + (Math.cos(toRadians(bulletAngle2)) * bulletSpeed);
				}
				else{
					bulletLeft2 = bulletLeft2 - (Math.cos(toRadians(bulletAngle2)) * bulletSpeed);
				}
				if(topflip2 == 0){
					bulletTop2 = bulletTop2 + (Math.sin(toRadians(bulletAngle2)) * bulletSpeed);
				}
				else{
					bulletTop2 = bulletTop2 - (Math.sin(toRadians(bulletAngle2)) * bulletSpeed);
				}
				io.sockets.emit('bullet2loc', {left:bulletLeft2, top:bulletTop2, angle:bulletAngle2});
			}, 25);
			setTimeout(function(){
				clearInterval(bullet2interval);
				bullet2interval = 0;
				shot2 = 0;
				if(hiddenbullet2==0){
					io.sockets.emit('bullet2hide');
					hiddenbullet2=1;
				}
			}, 12000);
		}
	});
	socket.on('topflip2', function(data){
		if(topflip2 == 0){
			topflip2 = 1;
		}
		else{
			topflip2 = 0;
		}
	});
	socket.on('leftflip2', function(data){
		if(leftflip2 == 0){
			leftflip2 = 1;
		}
		else{
			leftflip2 = 0;
		}
	});
	socket.on('topflip1', function(data){
		if(topflip1 == 0){
			topflip1 = 1;
		}
		else{
			topflip1 = 0;
		}
	});
	socket.on('leftflip1', function(data){
		if(leftflip1 == 0){
			leftflip1 = 1;
		}
		else{
			leftflip1 = 0;
		}
	});
	socket.on('reset', function(data){
		leftflip1 = 0;
		topflip1 = 0;
		leftflip2 = 0;
		topflip2 = 0;
		left = 60;	
		top = 60;	
		angle = 0;	
		left2 = 500; 
		top2 = 500;	
		angle2 = 180;
		shot1=0;
		shot2=0;
		if(bullet1interval != 0){
			clearInterval(bullet1interval);
			bullet1interval = 0;
		}
		if(bullet2interval != 0){
			clearInterval(bullet2interval);
			bullet2interval = 0;
		}
		if(hiddenbullet2==0){
			io.sockets.emit('bullet2hide');
			hiddenbullet2=1;
		}
		if(hiddenbullet1==0){
			io.sockets.emit('bullet1hide');
			hiddenbullet1=0;
		}
	});
});
