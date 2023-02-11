var myModal = new bootstrap.Modal(document.getElementById('exampleModal'), 'focus');

let time = 0;
$(document).ready(function () {
    //здесь функция срабатывает раз в минуту, можно настроить как вам удобно
    let interval = setInterval(idleTimer, 60000);
    //тут можно добавлять все события которые не должны срабатывать(нажатие на клавиши, ресайз и т.д.)
    $(this).on('mousemove', function (e) {
    time = 0;
    });
});

function idleTimer() {
    time = time + 1;
    if (time > 2) {
        //здесь нужное вам действие на простой
        myModal.show();
        timerload(15);
        let no = document.querySelector('#button_no');
        let yes = document.querySelector('#button_yes');
        yes.addEventListener('click', function() {
            history.back();
        });
        no.addEventListener('click', function() {
            myModal.hide();
        });
    };
};

function timer(t){
    if (t == 0){
      history.back();
    };
    document.getElementById('timedown').innerHTML = '' + t + ''
    console.log(t)
    setTimeout(() =>  timer(t - 1), 1000);
};