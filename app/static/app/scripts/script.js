$(function() {
    // опции для датапикера , даты и времени соотвественно
    var dt_picker_date = { language: 'ru', autoclose: true, format: "yyyy-mm-dd", minView: "month" };
    var dt_picker_time = { language: 'ru', autoclose: true, format: "HH:ii", startView: "day" };

    // скрываем сообщения , которые появляються
    $('.clsMessage').load().fadeOut(3000);

    // ссылка для редиректа
    var redirect_url = '/';
    
    // header таблиц скрываем при нажатии
    //первоначальное положение скрытое
    //$('.table-responsive').children().toggle();
    //// пока не делаем
    //var tables_for_togle = $('.table-name');
    //tables_for_togle.each(function () {
    //    $(this).siblings('.table-responsive').first().toggle();
    //});
    $('.table-name').click(function () {
        //console.log('table name toggle');
        $(this).siblings('.table-responsive').first().toggle();
    });
    // при нажатии плюсика открываем модаль , но запрещаем скрывать таблицу
    $('.table-name > h4 > span > img').click(function (event) {
        event.stopPropagation();        
        //console.log($(this).closest('.table-responsive'));
        $(this).closest('.table-responsive').next().modal();
    });

    // "Положение" , скрываем-раскрываем тело положений так же как в основном окне 
    var reglament_name = $('.reglament-name');
    // начальное положение , скрыты все положения
    reglament_name.next('div').toggle();
    reglament_name.click(function () {
        $(this).next('div').toggle();
    });

    ///Новости
    var news_detailed = $('.news_detailed');    
    news_detailed.click(function () {
        console.log($(this).siblings('.news-name'));
        var news_full = $(this).parent().siblings('.news-name').next().next();
        var news_trunk = $(this).parent().siblings('.news-name').next();

        if (news_full.hasClass('hidden')) {
            news_full.removeClass('hidden');
            news_trunk.addClass('hidden');
            $(this).text('Свернуть');
        }
        else {
            news_full.addClass('hidden');
            news_trunk.removeClass('hidden');
            $(this).text('Подробнее');
        }
        //console.log($(this).text());
    });

    //DIRECTOR  //редактирование Директора  
    var $EditDirectorFormId = $(document.getElementById('EditDirectorFormId'));//$('#EditDirectorFormId');
    var $region = $EditDirectorFormId.find('[name="region"]'),
        $city = $EditDirectorFormId.find('[name="city"]'),
        $street = $EditDirectorFormId.find('[name="street"]'),
        $building = $EditDirectorFormId.find('[name="homeNumber"]');

    $.kladr.setDefault({
        parentInput: $EditDirectorFormId.find('.js-form-address'),
        verify: true,
        select: function (obj) {
            setLabel($(this), obj.type);
            //$tooltip.hide();
            $('.deleteAfterResubmit').remove();
        },
        check: function (obj) {
            var $input = $(this);
            console.log('--check kladr--');
            if (obj) {
                setLabel($input, obj.type);
                //$tooltip.hide();
                $('.deleteAfterResubmit').remove();
            }
            else {
                console.log('Введено неверно');
                showError($input, 'Введено неверно');                
            }
        },
        checkBefore: function () {
            var $input = $(this);
            console.log('--before check kladr--');
            if (!$.trim($input.val())) {
                //$tooltip.hide();
                $('.deleteAfterResubmit').remove();
                return false;
            }
        }
    });

    $region.kladr('type', $.kladr.type.region);
    //$district.kladr('type', $.kladr.type.district);
    $city.kladr('type', $.kladr.type.city);
    $street.kladr('type', $.kladr.type.street);
    $building.kladr('type', $.kladr.type.building);

    // Отключаем проверку введённых данных для строений
    $building.kladr('verify', false);

    function setLabel($input, text) {
        text = text.charAt(0).toUpperCase() + text.substr(1).toLowerCase();
        $input.parent().find('label').text(text);
    }

    function showError($input, message) {
        $input.after('<div class="alert alert-danger small input-sm form-control \
                        deleteAfterResubmit">' + message + '</div>');

        //$tooltip.show();
    }
    
    //заполняем форму , НО НЕ ВСЕ поля (нужно для кладр) , а только регион , город 
    $('#EditDirectorModal').on('shown.bs.modal', function () {
        //var _url = $(this).find('form').attr("action");        
        var _url = "/api/v1/director/";   // работает через tastypie 2016.09.21 
        $.ajax({
            url: _url,
            dataType: 'json',
            success: function (data) {
                console.log(data);
                //var _data = $.parseJSON(data);                
                _data = data.objects[0]; //_data[0].fields;
                console.log(_data);
                $region.kladr('controller').setValue(_data['region']);
                $city.kladr('controller').setValue(_data['city']);
                if (_data.status === 'warn') {                    
                    _formId.children('.modal-body').before('<p class="alert alert-danger text-center container deleteAfterResubmit">' + _data.status_comment + '</p>');
                }
            },
            statusCode: {
                404: function () {
                    alert('There was a problem with the server. Try again soon!');
                }
            }
        });
    });

    // кнопка "загрузить фото"
    $('#profile_block > div:nth-child(1)').hover(
        function () { $('#profile_image_btn').css('z-index', '10') },
        function () { $('#profile_image_btn').css('z-index', '-10') }
    );    
    
    // кнопка Отмена в профиле , без модального окна , делаем редирект назад на стр регистрации    
    $('#profile_id').find('a.btn').attr('href', '/register/');
    
    // без модального окна    
    //check form by ajax before submitting
    $('#EditDirectorFormId').on('submit', function (e) {
        console.log('dir submit');
        // delete warnings
        $('.deleteAfterResubmit').remove();

        var _formId = $(this);
        e.preventDefault();
        var ser = _formId.find('input,select').serialize();
        console.log(e);

        $.post(_formId.attr('action'), ser, function (data) {
            if (data != 'ok') {
                console.log(data);
                console.log(data.formErrors);
                //var _err = $.parseJSON(data.formErrors);
                var _err = data.formErrors;
                var items = [];
                $.each(_err, function (key, val) {
                    $('#dir_' + key).after('<div class="alert alert-danger small input-sm form-control \
                        deleteAfterResubmit">' + val + '</div>');
                });
            }
            else {
                console.log('success for submitting');
                document.location.href = redirect_url;
            }
        });
    }); // EditDirectorFormId submitting
    //END of DIRECTOR

    ///MEMBER
    //когда закрываем модаль , очищаем все значения , которые присвоили раннее редактировав участника
    // возвращаем action url в исходное состояние
    $('#AddMemberModal').on('hidden.bs.modal',
        function () {
            funcMemberFormClear();
            //// delete warnings
            //$('.deleteAfterResubmit').remove();           

            //$('#member_age_group').val('');
            //$('#member_first_name').val('');
            //$('#member_last_name').val('');
            ////$('#member_MiddleName').val('');
            //$('#member_age').val('');
            //$('#member_gender').val('');
            //$('#member_scan_passport').val('');
            ////активируем кнопку Готово , после закрытия модального окна
            //$(this).find('input[type="submit"]').prop("disabled", false);
        }
    );

    //check form by ajax before submitting
    var AddMemberModal = $('#AddMemberModal');    
    //$('#MemberFormGotovo').on('click', function (e) {
    $('#AddMemberModal').on('submit', function (e) {
        console.log('submit button has been clicked');
        // delete warnings
        $('.deleteAfterResubmit').remove();

        var _formId = AddMemberModal.find('form');
        //делаем кнопку готово не активной , чтобы не нажать несколько раз . Активируем вконце проверки аяксом
        var btn_submit = AddMemberModal.find('input[type="submit"]');
        btn_submit.prop("disabled", true);

        startLoadingAnimation();
        //_formId.find('.modal-footer').children().first().before(<img id="loadImg" class="loadImg" src="{% static 'app/images/ajax-loader.gif'%}" />");
        //alert("Подождите, добавление участника займет какое-то время в зависимости от размера фотографии. Для продолжения нажмите 'Ок'");
              
        var fd = new FormData(document.querySelector("#AddorEditMemberFormId"));        
        $.ajax({
            url: _formId.attr('action'),
            type: "POST",
            data: fd,
            processData: false,  // tell jQuery not to process the data
            contentType: false,   // tell jQuery not to set contentType
            success: function (data) {
                if (data != 'ok') {
                    console.log('wrong - neOK submitting');
                    var _err = $.parseJSON(data.formErrors);
                    var items = [];
                    $.each(_err, function (key, val) {
                        $('#member_' + key).after('<div class="alert alert-danger small input-sm form-control \
                            deleteAfterResubmit">' + val + '</div>');
                        // if foto not uloaded yet , raise an exception
                        if (key === '__all__') {
                            $('#member_scan_passport').after('<div class="alert alert-danger small input-sm form-control \
                            deleteAfterResubmit">' + val + '</div>');
                        }                            
                    });
                    btn_submit.prop("disabled", false);
                    //stopLoadingAnimation();
                }
                else {                    
                    console.log('success submitting');                    
                    //document.location.href = redirect_url;                    
                    $.ajax({
                        url: "app/memberFrame/",
                        //async: true,
                        success: function (data) {                            
                            console.log('====before hide the modal===');
                            //document.location.href = redirect_url;
                            //AddMemberModal.hide();
                            AddMemberModal.modal('hide');                            
                            $('#TableMembersID').html(data);                          
                        },
                        error: function () {
                            console.log('something wrong - didnt get tables');
                            document.location.href = redirect_url;
                            //alert('Произошла ошибка, перезагрузите страницу')                            
                        }
                    });
                    //return false; // отменить переход по url
                }
            },
            error: function () {
                console.log('something wrong');      
                //stopLoadingAnimation();
            }
        });
        btn_submit.prop("disabled", false);
        stopLoadingAnimation();
        e.preventDefault();
        //return false;
    }); // End of AddorEditMemberFormId submitting

    //delete memeber
    var DelMemberModal = $('#DelMemberModal');
    $('#DelMemberModal').on('submit', function (e) {
        startLoadingAnimation();
        console.log('submit button has been clicked');
        // delete warnings
        $('.deleteAfterResubmit').remove();

        var _formId = DelMemberModal.find('form');;
        //делаем кнопку готово не активной , чтобы не нажать несколько раз . Активируем вконце проверки аяксом
        var btn_submit = DelMemberModal.find('input[type="submit"]');
        btn_submit.prop("disabled", true);        

        console.log(document.querySelector("#delMemberId"));
        var fd = new FormData(document.querySelector("#delMemberId"));
        $.ajax({
            url: _formId.attr('action'),
            type: "POST",
            data: fd,
            processData: false,  // tell jQuery not to process the data
            contentType: false,   // tell jQuery not to set contentType
            success: function (data) {
                if (data != 'ok') {
                    console.log('wrong - neOK submitting');
                    alert('Произошла ошибка, перезагрузите страницу');
                    //btn_submit.prop("disabled", false);
                    //stopLoadingAnimation();
                }
                else {
                    console.log('success submitting');
                    //document.location.href = redirect_url;                   
                    $.ajax({
                        url: "app/memberFrame/",
                        //async: true,
                        success: function (data) {
                            console.log('====before hide the modal===');
                            //document.location.href = redirect_url;
                            //DelMemberModal.hide();
                            DelMemberModal.modal('hide');                            
                            $('#TableMembersID').html(data);                            
                            btn_submit.prop("disabled", false);                            
                        },
                        error: function () {
                            console.log('something wrong');
                            document.location.href = redirect_url;
                            //alert('Произошла ошибка, перезагрузите страницу')
                            //stopLoadingAnimation();
                        }
                    });
                    //return false; // отменить переход по url
                }
            },
            error: function () {
                console.log('something wrong');                
            }
        });

        stopLoadingAnimation();
        e.preventDefault();
        return false;
    });

    //PARTICIPATION=======================================================================================================    
    var prtcp_category = $('#prtcp_category');
    var prtcp_nomination = $('#prtcp_nomination');
    var prtcp_age_group = $('#prtcp_age_group');
    var prtcp_form_of_execution = $('#prtcp_form_of_execution');
    function filter_participation() {
        prtcp_nomination.children('option[value="spec"]').addClass('hidden');
        //$('#prtcp_nomination option[value=""]').attr('selected', 'selected');

        if (prtcp_category.val() === 'adults') {            
            var adults_arr = ['', 'estrada', 'narod', 'narod_style', 'sovremen_svobod', 'sovremen_ulica'];
            $('#prtcp_nomination option').each(function () {
                $(this).removeClass('hidden');
                //if ($(this).val() === "spec") { $(this).addClass('hidden');  }
                if ($.inArray($(this).val(), adults_arr) === -1) {
                    $(this).addClass('hidden')
                }
            });
            if (prtcp_nomination.val() === 'spec') {
                prtcp_nomination.val("");
            }
            // обнуляем возраста
            prtcp_age_group.children('option').each(function () {
                $(this).removeClass('hidden');
                if ($.inArray($(this).val(), ['', '11-14', '15-18', '18-25', 'hybrid']) === -1) {
                    $(this).addClass('hidden');
                }
                else {
                    $(this).removeClass('hidden');
                }
            });
        }
        if (prtcp_category.val() === 'kids') {            
            var kids_arr = ['', 'estrada', 'narod+_narod_style', 'suget-igrovoi'];
            $('#prtcp_nomination option').each(function () {
                if (($.inArray($(this).val(), kids_arr)) === -1) {
                    $(this).addClass('hidden');
                }
                else {
                    $(this).removeClass('hidden');
                }
            });
            if (($.inArray(prtcp_nomination.val(), kids_arr)) === -1) {
                prtcp_nomination.val("");
            }
            prtcp_age_group.children('option').each(function () {                
                if ($.inArray($(this).val(), ['', '0-7', '8-10' ,'hybrid']) === -1) {
                    $(this).addClass('hidden');
                }
                else {
                    $(this).removeClass('hidden');
                }
            });
        }
        if (prtcp_category.val() === 'spec') {            
            $('#prtcp_nomination option').each(function () {                
                if ($(this).val() === "spec") { $(this).removeClass('hidden'); return }
                $(this).addClass('hidden');
            });            
            if (prtcp_nomination.val() !== 'spec') {                
                prtcp_nomination.val("");
            }
            // обнуляем возраста
            prtcp_age_group.children('option').each(function () {
                if (!($.inArray($(this).val(), ['0-7']) === -1)) {
                    $(this).addClass('hidden');
                }
                else {
                    $(this).removeClass('hidden');
                }
                //$(this).removeClass('hidden');
            });
        }        
    }
    // форма исполнения, при изменении , скрываем-показываем поля для ФИО
    function filter_form_execution() {
        console.log('---filter---');
        console.log(prtcp_form_of_execution.val());
        var that = prtcp_form_of_execution;
        if (that.val() == '') {
            $('#div_id_member1').addClass('hidden');
            $('#div_id_member2').addClass('hidden');
            $('#div_id_member3').addClass('hidden');
        }
        else if (that.val() == 'solo') {
            console.log('solo detected');
            $('#div_id_member1').removeClass('hidden');
            $('#div_id_member2').addClass('hidden');
            $('#div_id_member3').addClass('hidden');
        }
        else if (that.val() == 'duet') {
            console.log('duet detected');
            $('#div_id_member1').removeClass('hidden');
            $('#div_id_member2').removeClass('hidden');
            $('#div_id_member3').removeClass('hidden');
        }
        else {
            $('#div_id_member1').addClass('hidden');
            $('#div_id_member2').addClass('hidden');
            $('#div_id_member3').addClass('hidden');
        }
    }
    $('#AddParticipationModal').on('shown.bs.modal', function () {
        filter_participation();
        filter_form_execution();
    });
    //когда закрываем модаль , очищаем все значения , которые присвоили раннее редактировав участника
    // возвращаем action url в исходное состояние
    $('#AddParticipationModal').on('hidden.bs.modal',
        function () {
            $('.deleteAfterResubmit').remove();
            $('#prtcp_category').val('');
            $('#prtcp_nomination').val('');
            $('#prtcp_nomination option').each(function () {                
                $(this).removeClass('hidden');
            });
            $('#prtcp_age_group').val('');

            $('#prtcp_subgroup').val('');
            $('#prtcp_self_choice input').attr('checked', false);
            $('#prtcp_subgroup_inactive').attr('checked', false);
            $('#prtcp_form_of_execution').val('');

            $('#prtcp_list_member').val('');
            $('#prtcp_member_1').val('');
            $('#prtcp_member_2').val('');
            $('#prtcp_member_3').val('');
            //$('#prtcp_list_member').multiselect('deselectAll', true);
            //$('#prtcp_list_member').multiselect('updateButtonText');
            //$('#prtcp_member_count').text('0');

            //$('#div_id_list_member .controls label input').each(function (_obj) {
            //    //$(this).attr('checked', false);   
            //    $(this).removeAttr('checked');
            //});

            $('#prtcp_composition_1').val('');
            $('#prtcp_count_member_1').val('');
            $('#prtcp_composition_2').val('');
            $('#prtcp_count_member_2').val('');
            $('#prtcp_description_comp').val('');

            //активируем кнопку Готово , после закрытия модального окна
            $(this).find('input[type="submit"]').prop("disabled", false);
        }
    );
    // поле Категория   
    prtcp_category.change(function () { filter_participation() });
    // таблица Заявки на участие , поле Подгруппа коллектива
    $('.checkbox').addClass('input-sm');
    var prtcp_subgroup = $('#prtcp_subgroup');
    prtcp_subgroup.after('<div id="prtcp_self_choice"><input type="checkbox" class="" value="1">Свое название</div>');
    // когда нажимаем галочку Свой выбор , делаем простое поле без select
    var prtcp_self_choice = $('#prtcp_self_choice :checkbox');    
    prtcp_self_choice.change(function () {
        if ($(this).is(':checked')) {            
            prtcp_subgroup.addClass('hidden');
            prtcp_self_choice.before('<input class="input-sm form-control" id="prtcp_self_choice_text" name="subgroupSelf">');
        } else {            
            prtcp_subgroup.removeClass('hidden');
            $('#prtcp_self_choice_text').remove();
        }        
    });

    // кнопка - "Не учитывать в дипломе"
    $('#prtcp_self_choice').after('<input type="checkbox" class="" id="prtcp_subgroup_inactive" value="1">Не учитывать');
    var prtcp_subgroup_inactive = $('#prtcp_subgroup_inactive');
    prtcp_subgroup_inactive.change(function () {
        if ($(this).is(':checked')) {
            prtcp_subgroup.prop('disabled', true);
            $('#prtcp_self_choice_text').prop('disabled', true);
        } else {
            prtcp_subgroup.prop('disabled', false);
            $('#prtcp_self_choice_text').prop('disabled', false);
        }
    });

    prtcp_form_of_execution.change(function () {
        filter_form_execution();
    });
    // поле Список участников , при изменении считаем количество участников и сумму сбора
    //var paymentFunc = function () {        
    //    var _count = $('ul.multiselect-container > li > a > label > input[type="checkbox"]:checked').length;
    //    console.log($('ul.multiselect-container > li > a > label > input[type="checkbox"]:checked').length);        

    //    var prtcp_count = $('#prtcp_member_count');
    //    prtcp_count.text(_count);        
    //};
    //// поле мультиселекта до 2016.03.24
    //$('#prtcp_list_member').multiselect({        
    //    enableCollapsibleOptGroups: true,
    //    numberDisplayed: 0,
    //    onInitialized: paymentFunc,
    //    onChange: paymentFunc,        
    //});    

    ////счетчик участников и сумма для заявок на участие
    //$('#prtcp_list_member').next('.btn-group').after('<span> Кол-во участников</span> <span id="prtcp_member_count"></span>');
    //check form by ajax before submitting
    var AddParticipationModal = $('#AddParticipationModal');
    AddParticipationModal.on('submit', function (e) {
        // delete warnings
        $('.deleteAfterResubmit').remove();      
        startLoadingAnimation();
        var that = AddParticipationModal;
        var _formId = that.find('form');
        //делаем кнопку готово не активной , чтобы не нажать несколько раз . Активируем вконце проверки аяксом
        var btn_submit = _formId.find('input[type="submit"]');
        btn_submit.prop("disabled", true);
        var ser = _formId.find('input,select,textarea').serialize();                    
        console.log(ser);
        console.log("---ser---------");
        var fd = new FormData(document.querySelector("#AddorEditParticipationFormId"));
        $.ajax({
            url: _formId.attr('action'),
            async: false,
            type: "POST",
            data: fd,
            processData: false,  // tell jQuery not to process the data
            contentType: false,   // tell jQuery not to set contentType
            success: function (data) {
                if (data != 'ok') {
                    console.log(data.formErrors);
                    var _err = $.parseJSON(data.formErrors);
                    var items = [];
                    $.each(_err, function (key, val) {
                        $('#prtcp_' + key).after('<div class="alert alert-danger small input-sm form-control \
                        deleteAfterResubmit">' + val + '</div>');
                        // list member id is "list_member_0", therefore use this
                        //if (key === 'list_member') {
                        //    $('#div_id_list_member').after('<div class="alert alert-danger small input-sm form-control \
                        //deleteAfterResubmit">' + val + '</div>');
                        //}
                        if (key === '__all__') {
                            _formId.children('.modal-body').before('<p class="alert alert-danger text-center container deleteAfterResubmit">' + val + '</p>');
                            that.animate({ "scrollTop": 0 }, 100);
                        }
                    });
                }
                else {
                    console.log('success for submitting');                    
                    $.ajax({
                        url: "app/participationFrame/",
                        //async: true,
                        success: function (data) {
                            console.log('====before hide the modal===');                            
                            //AddMemberModal.hide();
                            that.modal('hide');
                            $('#TableParticipationsID').html(data);
                        },
                        error: function () {
                            console.log('something wrong - didnt get tables');
                            document.location.href = redirect_url;
                            //alert('Произошла ошибка, перезагрузите страницу')                            
                        }
                    });
                }
            },            
        });
        btn_submit.prop("disabled", false);
        stopLoadingAnimation();
        e.preventDefault();
    });

    //delete Participation
    var delParticipationModal = $('#DelParticipationModal');
    $('#DelParticipationModal').on('submit', function (event) {
        DeleteItem(delParticipationModal, "app/participationFrame/", $("#TableParticipationsID"), event)
    });
    // END of PARTICIPATION===================================================================================================

    // RESIDING , заполняем поля "Проживание" при загрузке модального окна============================== 
    $('#AddResidingModal').on('shown.bs.modal',
        function () {
            $("#rsd_date_arrival").datetimepicker(dt_picker_date);
            $("#rsd_time_arrival").datetimepicker(dt_picker_time);
            $("#rsd_date_departure").datetimepicker(dt_picker_date);
            $("#rsd_time_departure").datetimepicker(dt_picker_time);
        }
    );
    $('#AddResidingModal').on('hidden.bs.modal',
        function () {
            $(".deleteAfterResubmit").remove();

            $("#rsd_place_of_residing").val('');
            $("#rsd_quantity_total").val('');            
            $("#rsd_quantity_adult_male").val('');
            $("#rsd_quantity_adult_female").val('');
            $("#rsd_quantity_member_male").val('');
            $("#rsd_quantity_member_female").val('');
            $("#rsd_date_arrival").val('');
            $("#rsd_time_arrival").val('');
            $("#rsd_date_departure").val('');
            $("#rsd_time_departure").val('');
            //активируем кнопку Готово , после закрытия модального окна
            $(this).find('input[type="submit"]').prop("disabled", false);
        }
    );
    //check form by ajax before submitting
    var AddResidingModal = $('#AddResidingModal');
    $('#AddorEditResidingFormId').on('submit', function (event) {
        AddorEditSubmitForm(AddResidingModal, "app/residingFrame/", $("#TableResidingsID"), "#rsd_", event)
        //// delete warnings
        //$('.deleteAfterResubmit').remove();

        //var _formId = $(this);
        ////делаем кнопку готово не активной , чтобы не нажать несколько раз . Активируем вконце проверки аяксом
        //var btn_submit = _formId.find('input[type="submit"]');
        //btn_submit.prop("disabled", true);

        //e.preventDefault();
        //var ser = _formId.find('input,select').serialize();
        //console.log(e);

        //$.post(_formId.attr('action'), ser, function (data) {
        //    if (data != 'ok') {
        //        //console.log(data.formErrors);
        //        var _err = $.parseJSON(data.formErrors);
        //        var items = [];
        //        $.each(_err, function (key, val) {
        //            $('#rsd_' + key).after('<div class="alert alert-danger small input-sm form-control \
        //                deleteAfterResubmit">' + val + '</div>');
        //        });
        //        btn_submit.prop("disabled", false);
        //    }
        //    else {
        //        console.log('success for submitting');                
        //        document.location.href = redirect_url;             
        //    }
        //});
    }); // AddorEditResidingFormId submitting

    //delete Residing
    var delResidingModal = $('#DelResidingModal');
    $('#DelResidingModal').on('submit', function (event) {
        DeleteItem(delResidingModal, "app/residingFrame/", $("#TableResidingsID"), event)
    });
    // END of RESIDING===================================================================================

    // TRANSFER================================================================================================
    // прикручиваем виджет с датами   
    $('#AddTransferModal').on('shown.bs.modal',
        function () {
            $("#trans_date_departure").datetimepicker(dt_picker_date);
            $("#trans_time_departure").datetimepicker(dt_picker_time);
        }
    );
    $('#AddTransferModal').on('hidden.bs.modal',
        function () {
            $('.deleteAfterResubmit').remove();
            $("#trans_date_departure").val('');
            $("#trans_time_departure").val('');
            $("#trans_place_departure").val('');
            $("#trans_place_arrival").val('');
            $("#trans_quantity_total").val('');
            $("#trans_quantity_adult").val('');
            $("#trans_quantity_member").val('');
            //активируем кнопку Готово , после закрытия модального окна
            $(this).find('input[type="submit"]').prop("disabled", false);
        }
    );
    
    var trans_place_departure = $('#trans_place_departure');    
    trans_place_departure.after('<div id="trans_place_departure_self"><input type="checkbox" class="" value="1">Свое название</div>');
    // когда нажимаем галочку Свой выбор , делаем простое поле без select
    var trans_place_departure_self = $('#trans_place_departure_self :checkbox');
    trans_place_departure_self.change(function () {
        if ($(this).is(':checked')) {            
            trans_place_departure.addClass('hidden');
            trans_place_departure_self.before('<input class="input-sm form-control" id="trans_departure_self_text" name="transDepartureSelf">');
        } else {            
            trans_place_departure.removeClass('hidden');
            $('#trans_departure_self_text').remove();
        }  
    });

    var trans_place_arrival = $('#trans_place_arrival');
    trans_place_arrival.after('<div id="trans_place_arrival_self"><input type="checkbox" class="" value="1">Свое название</div>');
    // когда нажимаем галочку Свой выбор , делаем простое поле без select
    var trans_place_arrival_self = $('#trans_place_arrival_self :checkbox');
    trans_place_arrival_self.change(function () {
        if ($(this).is(':checked')) {
            trans_place_arrival.addClass('hidden');
            trans_place_arrival_self.before('<input class="input-sm form-control" id="trans_place_arrival_self_text" name="transArrivalSelf">');
        } else {
            trans_place_arrival.removeClass('hidden');
            $('#trans_place_arrival_self_text').remove();
        }
    });

    //check form by ajax before submitting
    var AddTransferModal = $('#AddTransferModal');
    $('#AddorEditTransferFormId').on('submit', function (event) {
        AddorEditSubmitForm(AddTransferModal, "app/transferFrame/", $("#TableTransfersID"), "#trans_", event)
        // delete warnings
        //$('.deleteAfterResubmit').remove();

        //var _formId = $(this);
        ////делаем кнопку готово не активной , чтобы не нажать несколько раз . Активируем вконце проверки аяксом
        //var btn_submit = _formId.find('input[type="submit"]');
        //btn_submit.prop("disabled", true);

        //e.preventDefault();
        //var ser = _formId.find('input,select').serialize();
        //console.log(e);

        //$.post(_formId.attr('action'), ser, function (data) {
        //    if (data != 'ok') {
        //        console.log(data.formErrors);
        //        var _err = $.parseJSON(data.formErrors);
        //        var items = [];
        //        $.each(_err, function (key, val) {
        //            $('#trans_' + key).after('<div class="alert alert-danger small input-sm form-control \
        //                deleteAfterResubmit">' + val + '</div>');
        //            if (key === '__all__') {
        //                _formId.children('.modal-body').before('<p class="alert alert-danger text-center container deleteAfterResubmit">' + val + '</p>');
        //                //$('#member_scan_passport').after('<div class="alert alert-danger small input-sm form-control \
        //                //        deleteAfterResubmit">' + val + '</div>');
        //            }
        //        });
        //        btn_submit.prop("disabled", false);
        //    }
        //    else {
        //        console.log('success for submitting');                
        //        //window.location.replace("/");
        //        document.location.href = redirect_url;
        //    }
        //});
    }); // AddorEditTransferFormId submitting

    //delete Transfer
    var delTransferModal = $('#DelTransferModal');
    $('#DelTransferModal').on('submit', function (event) {
        DeleteItem(delTransferModal, "app/transferFrame/", $("#TableTransfersID"), event)
    });
    // END of TRANSFER=========================================================================================================

    //EXCURSION---------------------------------------------------------------------------------------------------------------
    var AddExcursionModal = $('#AddExcursionModal');
    AddExcursionModal.on('shown.bs.modal',
        function () {
            $("#ex_date_departure").datetimepicker(dt_picker_date);    //({ format: "yyyy-mm-dd", pickTime: "False" });
            $("#ex_time_departure").datetimepicker(dt_picker_time);         //({ autoclose: true, format: "HH:ii", startView: "day" });
        }
    );
    AddExcursionModal.on('hidden.bs.modal',
        function () {
            $("#ex_tour_form").val('');
            $("#ex_date_departure").val('');
            $("#ex_time_departure").val('');
            $("#ex_place_departure").val('');
            $("#ex_place_arrival").val('');
            $("#ex_quantity_total").val('');
            $("#ex_quantity_adult").val('');
            $("#ex_quantity_member").val('');
            //активируем кнопку Готово , после закрытия модального окна
            $(this).find('input[type="submit"]').prop("disabled", false);
        }
    );

    var ex_place_departure = $('#ex_place_departure');
    ex_place_departure.after('<div id="ex_place_departure_self"><input type="checkbox" class="" value="1">Свое название</div>');
    // когда нажимаем галочку Свой выбор , делаем простое поле без select
    var ex_place_departure_self = $('#ex_place_departure_self :checkbox');
    ex_place_departure_self.change(function () {
        if ($(this).is(':checked')) {
            ex_place_departure.addClass('hidden');
            ex_place_departure_self.before('<input class="input-sm form-control" id="ex_place_departure_self_text" name="exDepartureSelf">');
        } else {
            ex_place_departure.removeClass('hidden');
            $('#ex_place_departure_self_text').remove();
        }
    });

    var ex_place_arrival = $('#ex_place_arrival');
    ex_place_arrival.after('<div id="ex_place_arrival_self"><input type="checkbox" class="" value="1">Свое название</div>');
    // когда нажимаем галочку Свой выбор , делаем простое поле без select
    var ex_place_arrival_self = $('#ex_place_arrival_self :checkbox');
    ex_place_arrival_self.change(function () {
        if ($(this).is(':checked')) {
            ex_place_arrival.addClass('hidden');
            ex_place_arrival_self.before('<input class="input-sm form-control" id="ex_place_arrival_self_text" name="exArrivalSelf">');
        } else {
            ex_place_arrival.removeClass('hidden');
            $('#ex_place_arrival_self_text').remove();
        }
    });

    //check form by ajax before submitting
    var AddExcursionModal = $('#AddExcursionModal');
    AddExcursionModal.on('submit', function (event) { //$('#AddorEditExcursionFormId')
        AddorEditSubmitForm(AddExcursionModal, "app/excursionFrame/", $("#TableExcursionsID"), "#ex_", event)
        //// delete warnings
        //$('.deleteAfterResubmit').remove();

        //var _formId = $(this);
        ////делаем кнопку готово не активной , чтобы не нажать несколько раз . Активируем вконце проверки аяксом
        //var btn_submit = _formId.find('input[type="submit"]');
        //btn_submit.prop("disabled", true);

        //e.preventDefault();
        //var ser = _formId.find('input,select').serialize();
        //console.log(e);

        //$.post(_formId.attr('action'), ser, function (data) {
        //    if (data != 'ok') {
        //        console.log(data.formErrors);
        //        var _err = $.parseJSON(data.formErrors);
        //        var items = [];
        //        $.each(_err, function (key, val) {
        //            $('#ex_' + key).after('<div class="alert alert-danger small input-sm form-control \
        //                deleteAfterResubmit">' + val + '</div>');
        //        });
        //        btn_submit.prop("disabled", false);
        //    }
        //    else {
        //        console.log('success for submitting');
        //        //window.location.replace("/");                
        //        document.location.href = redirect_url;                           
        //    }
        //});
    }); // AddorEditExcursionFormId submitting

    //delete excursion
    var delExcursionModal = $('#DelExcursionModal');
    $('#DelExcursionModal').on('submit', function (event) {
        DeleteItem(delExcursionModal, "app/excursionFrame/", $("#TableExcursionsID"), event)
    });
    //END of EXCURSION========================================================================================================

    //FOOD
    $('#AddFoodModal').on('shown.bs.modal',
        function () {
            $("#food_date").datetimepicker(dt_picker_date);            
        }
    );
    $('#AddFoodModal').on('hidden.bs.modal',
        function () {
            $(".deleteAfterResubmit").remove();

            $("#food_place_of_residing").val('');
            $("#food_quantity_total").val('');
            $("#food_quantity_adult").val('');            
            $("#food_quantity_member").val('');
            $("#food_zavtrak").prop("checked", false);
            $("#food_obed").prop("checked", false);
            $("#food_ugin").prop("checked", false);
            $("#food_date").val('');           
            //активируем кнопку Готово , после закрытия модального окна
            $(this).find('input[type="submit"]').prop("disabled", false);
        }
    );
    //check form by ajax before submitting
    var AddFoodModal = $('#AddFoodModal');
    $('#AddorEditFoodFormId').on('submit', function (event) {
        AddorEditSubmitForm(AddFoodModal, "app/foodFrame/", $("#TableFoodsID"), "#food_", event)        
    }); 

    //delete Food
    var delFoodModal = $('#DelFoodModal');
    $('#DelFoodModal').on('submit', function (event) {
        DeleteItem(delFoodModal, "app/foodFrame/", $("#TableFoodsID"), event)
    });
    // end of FOOD
});
// END LOAD================================
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

// добавление участника 
function funcMemberAdd(obj) {
    $('#AddMemberModal').modal('toggle'); //return false;
}
function funcMemberRemove(obj) {
    //выводим в ворму Фамилию и Имя 
    $('#clsDelMemberId').text(($(obj).closest('tr').children('td:nth-child(3)').text()) + " " + $(obj).closest('tr').children('td:nth-child(4)').text());
    // делаем в модальной форме аргумент для acion урл плюс юзер id
    //замеяем часть урла 999999 на то что id который находиться рядом скрестиком и имеет класс hidden
    $('#delMemberId').attr("action", $('#delMemberId').attr("action").replace(/[0-9]+/, $(obj).children('.hidden').text()));
}

function funcMemberEdit(obj) {
    var AddorEditMemberFormId = $('#AddorEditMemberFormId');
    AddorEditMemberFormId.find('input[type="submit"]').prop("disabled", false);
//    // делаем в модальной форме аргумент для action урл плюс юзер id
//    //замеяем часть урла 999999 на то что id который находиться рядом скрестиком и имеет класс hidden//     
    //$('#AddorEditMemberFormId').attr("action", $('#AddorEditMemberFormId').attr("action").replace(/[0-9]+/i, $(obj).next().children('.hidden').text()));
    //заполняем форму значениями из таблицы, соответсвующие текущему редактируемому пользователю    
    Edit(obj, AddorEditMemberFormId, 'app/createOrEditMember/', 'member_');
}

// очистка формы при закрытии и добавлении
function funcMemberFormClear(obj) {
    var AddorEditMemberFormId = $('#AddorEditMemberFormId');
    AddorEditMemberFormId.find('input[type="submit"]').prop("disabled", false);
    // delete warnings
    $('.deleteAfterResubmit').remove();

    $('#member_age_group').val('');
    $('#member_first_name').val('');
    $('#member_last_name').val('');
    //$('#member_MiddleName').val('');
    $('#member_age').val('');
    $('#member_gender').val('');
    $('#member_scan_passport').val('');
}

//PArticipation =================
function funcParticipationAdd(obj) {
    // при открытии чистой модали изменяем урл на дефолтный
    var _formId = $('#AddorEditParticipationFormId');
    _formId.attr("action", _formId.attr("action").replace(/[0-9]+/i, '999999'));
}

function funcParticipationEdit(obj) {
    
    var _formId = $('#AddorEditParticipationFormId');
    //$('#AddorEditParticipationFormId').attr("action", $('#AddorEditParticipationFormId').attr("action").replace(/[0-9]+/i, $(obj).next().children('.hidden').text()));
    //Edit(obj, AddorEditParticipationFormId, 'app/createOrEditParticipation/', 'prtcp_');
    var _url = 'app/createOrEditParticipation/';
    var _url_id = $(obj).next().children('.hidden').text();
    var _prefix = 'prtcp_';
    _formId.attr("action", _formId.attr("action").replace(/[0-9]+/i, _url_id));
    $.ajax({
        url: _url + _url_id, async: false,
        dataType: 'json',
        success: function (data) {
            console.log(data);
            var _data = $.parseJSON(data);
            _data = _data[0].fields;
            jQuery.each(_data, function (key, value) {
                $('#' + _prefix + key).val(value);
                if (key === 'list_member') {
                    console.log(key);
                    console.log(value);
                    //$('#prtcp_list_member').multiselect('select', value, true);  // flag true for triggerOnChange;
                }
            });
            if (_data.status === 'warn') {
                //console.log(_data.status_comment);
                //_formId.children('.modal-body').addClass('ddd3333');
                _formId.children('.modal-body').before('<p class="alert alert-danger text-center container deleteAfterResubmit">' + _data.status_comment + '</p>');
            }
        },
        statusCode: {
            404: function () {
                alert('There was a problem with the server. Try again soon!');
            }
        }
    });
}

function funcParticipationRemove(obj) {
    //выводим в форму Номер заявки
    $('#clsParticipationId').text(($(obj).closest('tr').children('td:nth-child(1)').text()));

    $('#delParticipationFormId').attr("action", $('#delParticipationFormId').attr("action").replace(/[0-9]+/i, $(obj).children('.hidden').text()));
}            

//Residing
function funcResidingAdd(obj) {
    // при открытии чистой модали изменяем урл на дефолтный
    var _formId = $('#AddorEditResidingFormId');
    _formId.attr("action", _formId.attr("action").replace(/[0-9]+/i, '999999'));
}
function funcResidingEdit(obj) {
    var AddorEditResidingFormId = $("#AddorEditResidingFormId");
    //$("#AddorEditResidingFormId").attr("action", $("#AddorEditResidingFormId").attr("action").replace(/[0-9]+/i, $(obj).next().children('.hidden').text()));

    //var _residing_id = $(obj).next().children('.hidden').text();
    Edit(obj, AddorEditResidingFormId, 'app/createOrEditResiding/', 'rsd_');    
}
function funcResidingRemove(obj) {
    //выводим в форму Номер заявки
    $('#DelResidingId').text(($(obj).closest('tr').children('td:nth-child(1)').text()));
    var delResidingFormId = $('#delResidingFormId');
    delResidingFormId.attr("action", delResidingFormId.attr("action").replace(/[0-9]+/i, $(obj).children('.hidden').text()));
}

//Transfer
function funcTransferAdd(obj) {
    // при открытии чистой модали изменяем урл на дефолтный
    var _formId = $('#AddorEditTransferFormId');
    _formId.attr("action", _formId.attr("action").replace(/[0-9]+/i, '999999'));
}
function funcTransferEdit(obj) {
    var AddorEditTransferFormId = $("#AddorEditTransferFormId");
    //$("#AddorEditTransferFormId").attr("action", $("#AddorEditTransferFormId").attr("action").replace(/[0-9]+/i, $(obj).next().children('.hidden').text()));
    Edit(obj, AddorEditTransferFormId, 'app/createOrEditTransfer/', 'trans_');
}
function funcTransferRemove(obj) {
    //выводим в форму Номер заявки
    $('#DelTransferId').text(($(obj).closest('tr').children('td:nth-child(1)').text()));
    var delTransferFormId = $('#delTransferFormId');
    delTransferFormId.attr("action", delTransferFormId.attr("action").replace(/[0-9]+/i, $(obj).children('.hidden').text()));
}

//Excursion
function funcExcursionAdd(obj) {
    // при открытии чистой модали изменяем урл на дефолтный
    var _formId = $('#AddorEditExcursionFormId');
    _formId.attr("action", _formId.attr("action").replace(/[0-9]+/i, '999999'));
}
function funcExcursionEdit(obj) {
    var AddorEditExcursionFormId = $("#AddorEditExcursionFormId");
    //AddorEditExcursionFormId.attr("action", AddorEditExcursionFormId.attr("action").replace(/[0-9]+/i, $(obj).next().children('.hidden').text()));
    Edit(obj, AddorEditExcursionFormId, 'app/createOrEditExcursion/', 'ex_');  
}
function funcExcursionRemove(obj) {
    //выводим в форму Номер заявки
    $('#DelExcursionId').text(($(obj).closest('tr').children('td:nth-child(1)').text()));
    var delExcursionFormId = $('#delExcursionFormId');
    delExcursionFormId.attr("action", delExcursionFormId.attr("action").replace(/[0-9]+/i, $(obj).children('.hidden').text()));
}

//Food
function funcFoodAdd(obj) {
    // при открытии чистой модали изменяем урл на дефолтный
    var _formId = $('#AddorEditFoodFormId');
    _formId.attr("action", _formId.attr("action").replace(/[0-9]+/i, '999999'));
}
function funcFoodEdit(obj) {
    var AddorEditFoodFormId = $("#AddorEditFoodFormId");
    //$("#AddorEditFoodFormId").attr("action", $("#AddorEditFoodFormId").attr("action").replace(/[0-9]+/i, $(obj).next().children('.hidden').text()));

    //var _Food_id = $(obj).next().children('.hidden').text();
    //Edit(obj, AddorEditFoodFormId, 'app/createOrEditFood/', 'food_');
    var _formId = AddorEditFoodFormId;
    var _url = 'app/createOrEditFood/';
    var _url_id = $(obj).next().children('.hidden').text();
    var _prefix = 'food_';
    _formId.attr("action", _formId.attr("action").replace(/[0-9]+/i, _url_id));
    $.ajax({
        url: _url + _url_id, async: false,
        dataType: 'json',
        success: function (data) {
            console.log(data);
            var _data = $.parseJSON(data);
            _data = _data[0].fields;
            jQuery.each(_data, function (key, value) {
                $('#' + _prefix + key).val(value);
                //console.log(key);
                if ((key.match(/zavtrak/) !== null) || (key.match(/obed/) !== null) || key.match(/ugin/) !== null) {
                    $('#' + _prefix + key).prop("checked", value);
                    console.log(key);
                    console.log(value);                    
                }
            });
            if (_data.status === 'warn') {                
                _formId.children('.modal-body').before('<p class="alert alert-danger text-center container deleteAfterResubmit">' + _data.status_comment + '</p>');
            }
        },
        statusCode: {
            404: function () {
                alert('There was a problem with the server. Try again soon!');
            }
        }
    });
}
function funcFoodRemove(obj) {
    //выводим в форму Номер заявки
    $('#DelFoodId').text(($(obj).closest('tr').children('td:nth-child(1)').text()));
    var delFoodFormId = $('#delFoodFormId');
    delFoodFormId.attr("action", delFoodFormId.attr("action").replace(/[0-9]+/i, $(obj).children('.hidden').text()));
}

function Edit(obj, _formId, _url, _prefix) {
    var _url_id = $(obj).next().children('.hidden').text();   

    _formId.attr("action", _formId.attr("action").replace(/[0-9]+/i, _url_id));
    $.ajax({
        url: _url + _url_id,
        dataType: 'json',
        success: function (data) {
            //console.log(data);
            var _data = $.parseJSON(data);
            _data = _data[0].fields;            
            jQuery.each(_data, function (key, value) {               
                $('#' + _prefix + key).val(value);                
            });
            if (_data.status ==='warn') {  
                //console.log(_data.status_comment);
                //_formId.children('.modal-body').addClass('ddd3333');
                _formId.children('.modal-body').before('<p class="alert alert-danger text-center container deleteAfterResubmit">' + _data.status_comment + '</p>');
            }            
        },
        statusCode: {
            404: function () {
                alert('There was a problem with the server. Try again soon!');
            }
        }
    });
}

//delete items from Table
//var DelMemberModal = $('#DelMemberModal');

//$('#DelMemberModal').on('submit', function (e) {
function DeleteItem(modalId, urlForTable, objReplaceID, event) { //urlforTable - url который заменяется даными objReplaceID из запроса
    startLoadingAnimation();
    console.log('submit button has been clicked');
    // delete warnings
    $('.deleteAfterResubmit').remove();

    var _formId = modalId.find('form');
    //делаем кнопку готово не активной , чтобы не нажать несколько раз . Активируем вконце проверки аяксом
    var btn_submit = _formId.find('input[type="submit"]');
    btn_submit.prop("disabled", true);

    $.ajax({
        url: _formId.attr('action'),
        type: "POST",
        data: {csrfmiddlewaretoken: _formId.find('input[name=csrfmiddlewaretoken]').val() },
        success: function (data) {
            if (data != 'ok') {
                console.log('wrong - neOK submitting');
                document.location.href = "/";
            }
            else {
                console.log('success submitting');                               
                $.ajax({
                    url: urlForTable, //"app/memberFrame/",
                    async: false,
                    success: function (data) {
                        console.log('====before hide the modal===');
                        //document.location.href = redirect_url;                        
                        modalId.modal('hide');
                        objReplaceID.html(data);
                        //$('#TableMembersID').html(data);                        
                    },
                    error: function () {
                        console.log('something wrong');
                        document.location.href = "/";
                        //alert('Произошла ошибка, перезагрузите страницу')                        
                    }
                });               
            }
        },
        error: function () {
            console.log('something wrong');
        }
    });
    btn_submit.prop("disabled", false);
    stopLoadingAnimation();
    event.preventDefault();
    return false;
};

//функция при сабмите
function AddorEditSubmitForm(modalId, urlForTable, objReplaceID, prefix, event) { //prefix = '#rsd_'
    // delete warnings
    $('.deleteAfterResubmit').remove();
    console.log(modalId);
    var _formId = modalId.find('form');
    //делаем кнопку готово не активной , чтобы не нажать несколько раз . Активируем вконце проверки аяксом
    var btn_submit = _formId.find('input[type="submit"]');
    btn_submit.prop("disabled", true);
    startLoadingAnimation();

    var ser = _formId.find('input,select').serialize();
    ser['csrfmiddlewaretoken'] = _formId.find('input[name=csrfmiddlewaretoken]').val();
    console.log(ser);
    console.log("after serialization================")
    $.ajax({
        url: _formId.attr('action'), type: "POST", async: false,
        data: ser,
        success: function (data) {
            if (data != 'ok') {
                var _err = $.parseJSON(data.formErrors);
                console.log(_err);
                $.each(_err, function (key, val) {
                    $(prefix + key).after('<div class="alert alert-danger small input-sm form-control \
                            deleteAfterResubmit">' + val + '</div>');
                    if (key === '__all__') {
                        _formId.children('.modal-body').before('<p class="alert alert-danger text-center container deleteAfterResubmit">' + val + '</p>');
                        $('#member_scan_passport').after('<div class="alert alert-danger small input-sm form-control \
                                deleteAfterResubmit">' + val + '</div>');
                        modalId.animate({ "scrollTop": 0 }, 100);
                    }
                });
            }
            else {
                console.log('success for submitting');
                $.ajax({
                    url: urlForTable, //"app/memberFrame/",                
                    async: false,
                    success: function (data) {
                        console.log('====before hide the modal===');
                        //document.location.href = redirect_url;                        
                        modalId.modal('hide');
                        objReplaceID.html(data);
                        //$('#TableMembersID').html(data);                        
                    },
                    error: function () {
                        console.log('something wrong');
                        document.location.href = "/";
                        //alert('Произошла ошибка, перезагрузите страницу')                        
                    }
                });
            }
        },
        error: function (jqXHR, textStatus) {
            console.log('something wrong');
            console.log(jqXHR);
            console.log(textStatus);
            //document.location.href = "/";
        }
    });
    btn_submit.prop("disabled", false);
    stopLoadingAnimation();
    event.preventDefault();
    return false;
} 

//запуск и пауза музыки
function playMusic(obj) {
    console.log($(obj));
    var pl_obj = $(obj).children().last()[0];  //next()[0];  //siblings('.player');
    console.log(pl_obj);
    var player = pl_obj; //$(obj).next();   //siblings('.player'); //document.getElementById('player');
    (player.paused == true) ? toggle(0, player) : toggle(1, player);
}

function toggle(state, obj) {

    var player = $(obj)[0]; //document.getElementById('player');
    console.log("--ain toggle--");
    console.log(player);    
    var src = $(obj).attr('src');
    console.log(src);
    var playerIcon = $(obj).closest('td');
    console.log(playerIcon);

    switch (state) {
        case 0:
            playerIcon.children().first().css("display", "none");
            playerIcon.children('img').last().css("display", "block");
            player.src = src;
            player.load();
            player.play();
            player.innerHTML = 'Pause';
            player_state = 1;
            break;
        case 1:
            playerIcon.children().first().css("display", "block");
            playerIcon.children('img').last().css("display", "none");
            player.pause();
            player.currentTime = 0;
            //player.src = '';
            player.innerHTML = 'Play';
            player_state = 0;
            break;
    }
}