var myModal = new bootstrap.Modal(document.getElementById('exampleModal'), 'focus');

let time = 0;
$(document).ready(function () {
    //здесь функция срабатывает раз в минуту, можно настроить как вам удобно
    let interval = setInterval(idleTimer, 1000);
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
        let no = document.querySelector('#no');
        let yes = document.querySelector('#yes');
        yes.addEventListener('click', function() {
            history.back();
        });
        no.addEventListener('click', function() {
            myModal.hide();
        });
         timerload(15)
    };
};

function timerload(t){
    if (t == 0){
      history.back();
    };
    document.getElementById('no').innerHTML = 'Нет (' + t + ')'
    setTimeout(() =>  timerload(t - 1), 1000);
};