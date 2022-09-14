const video = document.getElementById('video');
const errorMsgElement = document.getElementById('span#ErrorMsg');
const constraints = {
video:{
        width: 1280, height: 720
      }
};
async function init(){
try{
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        handleSuccess(stream)
    }
    catch(e){
        errorMsgElement.innerHTML = 'navigator.getUserMedia.error:${e.toString()}';
    }
}
function handleSuccess(stream){
    window.stream = stream;
    video.srcObject = stream;
}
init();
var context = canvas.getContext('2d')
context.translate(canvas.width, 0);
context.scale(-1, 1);
snap.addEventListener('click', function(){
    context.drawImage(video, 0, 0, 1280, 720);
    console.log(canvas.toDataURL('image/png').split(',')[1])
//    $.ajax({
//      url: "/send",
//      method: "post",
//      data: {"image": canvas.toDataURL('image/png').split(',')[1]}
//      context: document.body
//    }).done(function() {
//      $(this).addClass("done");
//    });
//    var utf8 = atob(canvas.toDataURL('image/png').split(',')[1]);
//    function base64toblob(base64){
//        var utf8 = atob(base64),
//        array = [];
//        //---
//        for(var i = 0, j = utf8.length; i < j; i++)
//        array.push(utf8.charCodeAt(i));
//        //---
//        return(new Blob([new Uint8Array(array)], {type: 'image/png'}));
//    }
//    console.log(base64toblob(canvas.toDataURL('image/png').split(',')[1]), 'image_from_camera.png');
});