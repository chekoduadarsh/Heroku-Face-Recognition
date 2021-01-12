$(document).ready(function(){
  let namespace = "/test";
  let video = document.querySelector("#videoElement");
  let canvas = document.querySelector("#canvasElement");
  let ctx = canvas.getContext('2d');
  //let canvas2 = document.querySelector('#canvasElement2');
  //let ctx2 = canvas2.getContext('2d');
  photo = document.getElementById('photo');
    ctx.fillStyle = "blue";
    //ctx2.fillStyle = "blue";
  var localMediaStream = null;

  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
  //var socket = io(namespace);

  function readCamera() {
    ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, 300, 150);

  }

   /*function drawctx2(img){
   ctx2.drawImage(img,0,0)
   }*/

function sendSnapshot() {
    if (!localMediaStream) {
      return;
    }

    ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, 300, 150);



    let frame = ctx.getImageData(0, 0, 640, 480);
    //console.log(video.width, video.height)
    let dataURL = canvas.toDataURL('image/jpeg');
    socket.emit('input image', dataURL);


    socket.emit('output image')
    //console.log("call for out")

    var img = new Image();
    socket.on('out-image-event',function(data){
    //console.log(dataURL)
    //console.log(data.image_data)

    img.src = dataURL//data.image_data
    photo.setAttribute('src', data.image_data);
    //drawctx2(img)
    //ctx2.drawImage(img,0,0)
    });


  }

  socket.on('connect', function() {
    console.log('Connected!');
  });

  var constraints = {
    video: {
      width: { min: 640 },
      height: { min: 480 }
    }
  };

  navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
    video.srcObject = stream;
    localMediaStream = stream;
     document.getElementById("Capture").addEventListener("click", function() {
     sendSnapshot();
     });
    setInterval(function () {
      readCamera();
      //sendSnapshot();
    }, 50);
  }).catch(function(error) {
    console.log(error);
  });
});