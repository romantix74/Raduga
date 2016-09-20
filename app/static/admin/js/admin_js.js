$(function() {
    
    // кнопка для генерации дипломов
    var generate_place_btn_id = $('#generate_place_btn_id');
    generate_place_btn_id.on('click', function (e) {
        startLoadingAnimation();
        var that = generate_place_btn_id;
        _url = that.parent('form').attr('action');
        var _data = {};
        _data['csrfmiddlewaretoken'] = getCookie('csrftoken');
        console.log(_data);
        $.ajax({
            url: _url, type: "POST", async: false,
            data: _data,
            success: function (return_data) {
                console.log(return_data);
                if (return_data == 'ok') {
                    alert("Файлы дипломов сгенерированы");
                }
                else {
                    alert("Что-то пошло не так, уточните у админа ");
                }
            },
            statusCode: {
                404: function () {
                    alert('There was a problem with the server. Try again soon!');
                }
            },
            error: function (jqXHR, textStatus) {
                console.log('something wrong');
                console.log(jqXHR);
                console.log(textStatus);
            }
        });
        stopLoadingAnimation();
        e.preventDefault();
        return false;
    });

    // кнопка копирования музыки по номинациям
    var cp_music_btn_id = $('#cp_music_btn_id');
    cp_music_btn_id.on('click', function (e) {
        startLoadingAnimation();
        var that = cp_music_btn_id;
        _url = that.parent('form').attr('action');
        var _data = {};
        _data['csrfmiddlewaretoken'] = getCookie('csrftoken');
        console.log(_data);
        $.ajax({
            url: _url, type: "POST", async: false,
            data: _data,
            success: function (return_data) {
                console.log(return_data);
                if (return_data == 'ok') {
                    alert("Файлы аудиозаписей скопированы");
                }
                else {
                    alert("Что-то пошло не так, уточните у админа ");
                }
            },
            statusCode: {
                404: function () {
                    alert('There was a problem with the server. Try again soon!');
                }
            },
            error: function (jqXHR, textStatus) {
                console.log('something wrong');
                console.log(jqXHR);
                console.log(textStatus);
            }
        });
        stopLoadingAnimation();
        e.preventDefault();
        return false;
    });

    // Редактирование при нажатии на поле "место"
    //$('.hover').click(function () {
    //    console.log($(this).text());
    //    $(this).children().replaceWith("<input value=' " + $(this).text() + "'>");
    //    $(this).children().focus();
    //    $(this).children().click(function (event) {
    //        event.preventDefault();
    //    });
    //});

    //$(".hover").editable("click", function (e) {
    //    that = $(this);
    //    alert(that.value);
    //});
    // место для участников
    $(".hover").on('click', function () {
        that = $(this);
        console.log(that);
        console.log(that.next().text());
        that.editable('click', function (e) {
            _participation_id = that.next().text();
            var _data = {};
            _data['csrfmiddlewaretoken'] = getCookie('csrftoken');
            _data['participation_id'] = _participation_id;
            _data['place'] = e.value;
            console.log(e.value);
            console.log("/admin/app/participation/place/" ); //+ _participation_id + "-" + e.value + "/");
            $.ajax({
                url: "/admin/app/participation/place/", //+ _participation_id + "-" + e.value + "/",
                type: "POST",
                data: _data,
                success: function (return_data) {
                    console.log(return_data);
                    if (return_data == 'ok') {
                        console.log("обновлено");
                    }
                    else {
                        alert("Что-то пошло не так, уточните у админа ");
                    }
                },
                statusCode: {
                    404: function () {
                        alert('There was a problem with the server. Try again soon!');
                    }
                },
                error: function (jqXHR, textStatus) {
                    console.log('something wrong');
                    console.log(jqXHR);
                    console.log(textStatus);
                }
            });
        });
    });

    //сумма заявок
    $("#SummaId").text('0');
    getSum();
});
// END LOAD================================

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
//var csrftoken = getCookie('csrftoken');

function getSum() {
    var field_payment = $(".field-payment");
    var _sum = 0;
    $.each(field_payment, function (key, val) {
        _sum += parseInt($(val).text().replace(',0', ''), 10);
        $("#SummaId").text(_sum);
    });
}

function startLoadingAnimation() // - функция запуска анимации
{
    console.log("startAnimation");
    // найдем элемент с изображением загрузки и уберем невидимость:
    var imgObj = $(".loadImg");
    imgObj.show();

    // вычислим в какие координаты нужно поместить изображение загрузки,
    // чтобы оно оказалось в серидине страницы:
    var centerY = $(window).scrollTop() + ($(window).height() + imgObj.height()) / 2;
    var centerX = $(window).scrollLeft() + ($(window).width() + imgObj.width()) / 2;

    // поменяем координаты изображения на нужные:
    imgObj.offset({ top: centerY, left: centerX });
}

function stopLoadingAnimation() // - функция останавливающая анимацию
{
    console.log("stopAnimation");
    $(".loadImg").hide();
}