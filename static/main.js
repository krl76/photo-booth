transition.addEventListener('click', function(){
    var childWindow = window.open('camera');
    setTimeout(function () {
    childWindow.close();
    }, 5000);
});
