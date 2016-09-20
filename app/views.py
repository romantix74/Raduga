# -*- coding: utf-8 -*-
"""
Definition of views.
"""

from django.shortcuts import render, render_to_response ,redirect , get_object_or_404 
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.http import HttpRequest
from django.template import RequestContext , Context
from datetime import datetime
from django.http.response import HttpResponse
from django.template.loader import get_template
from models import Member, Director, News, Participation, Residing, Transfer, Tours, \
                   Excursion, Subgroup_choices, Place_departure_choices, Food, Mails,\
                   Album, Foto

from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import send_mail

from django.contrib.auth.forms import UserCreationForm
#from django.core.context_processors import csrf  # deprecated in 1.10
from django.template.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from forms import UserRegistrationForm, MemberForm , ParticipationForm , DirectorUploadFile , DirectorEditForm ,\
                  ResidingForm , TransferForm , ExcursionForm, FeedbackForm , FoodForm
from django.contrib import messages
import simplejson
from django.core import serializers
from django.views.decorators.csrf import csrf_protect

from django.views.generic import View, TemplateView

from django.template.loader import render_to_string

from app.engine.calc import Calc

from app.admin import return_list_filtered_by_form



# пока не нужно , испо-ся для отправки рендерных писем
#from django.template.loader import render_to_string

# проживание 
fee_residing = 100 # это пока тестовый платеж
# трансфер
fee_transfer = 100 # это пока тестовый платеж
# экскурсии
fee_excursion = 100 # это пока тестовый платеж


# json helpers
def _json_response(data):
    return HttpResponse(simplejson.dumps(data), content_type='application/json')

def _form_errors(form):    
    _message = u'Неправильно заполнена форма.' 
    response_data = {} # словарь для JSON-ответа
    response_data['errors']  = _message
    response_data['formErrors'] = form.errors
    #response_data = {'formErrors':form.errors}
    return _json_response(response_data)

#def _form_values(form):
#    values = {}
#    for field in form:
#        values[field.name] = field.value()
#    return _json_response({'values':values})

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    args = {}
    args['formFeedback'] = FeedbackForm()
    args['title'] = u'Контактная информация'
    args['year'] = datetime.now().year
    if request.POST:
        _form = FeedbackForm(request.POST) 
        if _form.is_valid():
            user_mail       = _form.cleaned_data['user_mail']  
            user_question   = _form.cleaned_data['user_question']
            #отправляем админам письмо о создании коллектива 
            _mails = User.objects.filter(is_superuser = 1).values_list('email', flat=True)
            for mail in _mails:
                try:
                    print "debug====================="
                    send_mail(u'Вопрос от: {0}'.format(user_mail), u'{0}'.format(user_question),
                              'dance@radugafest.com', [mail], fail_silently=False)
                except Exception as ex:
                    print ex.message 
            messages.add_message(request, messages.SUCCESS, u'Ваш запрос отправлен')
            return redirect(reverse('contact'))   #return redirect('/');       
        else:
            # если что то не так , то выводим форму с ошибками
            args['formFeedback'] = _form
    return render(
        request,
        'app/contact.html',
        args #context_instance = RequestContext(request, args)
    )

# результаты первого дня - ДЕТИ
def template_args_child(_age_prefix , _prefix_t , rnd_flag = False):
    _nom_list = ['estrada', 'narod+_narod_style', 'suget_igrovoi', 'spec']         
    _return_dict = {} # словарь из листов для перебора в шаблоне

    _args = {}        # хранение переменных для шаблона    
    _p = Participation.objects.filter(age_group=_age_prefix, place__isnull=False).exclude(place='') 
    _args['age_' + _prefix_t]               = _p      
    _args['age_' + _prefix_t + '_estrada']  = return_list_filtered_by_form(_p.filter(nomination = 'estrada'), rnd_flag)
    _return_dict[_nom_list[0]] = _args['age_' + _prefix_t + '_estrada']
        
    _args['age_' + _prefix_t + '_narod']    = return_list_filtered_by_form(
        _p.filter(nomination__contains='narod'), rnd_flag)    
        #_p.filter(nomination ='narod+_narod_style'), rnd_flag) 
    _return_dict[_nom_list[1]] = _args['age_' + _prefix_t + '_narod']
    _args['age_' + _prefix_t + '_suget_igrovoi'] = return_list_filtered_by_form(_p.filter(nomination = 
                                                                                            'suget-igrovoi'), rnd_flag)             
    _return_dict[_nom_list[2]] = _args['age_' + _prefix_t + '_suget_igrovoi']
    _args['age_' + _prefix_t + '_spec']     = return_list_filtered_by_form(_p.filter(nomination = 
                                                                                    'spec'), rnd_flag)   
    _return_dict[_nom_list[3]] = _args['age_' + _prefix_t + '_spec']
    _args['age_' + _prefix_t + '_list'] = _return_dict   
    return _args

def template_args_adults(_age_prefix , _prefix_t, rnd_flag = False):  # в шаблоне нельзя использовать знак "-" поэтому указываю сам префикс
        _args = {}      
        _p = Participation.objects.filter(age_group=_age_prefix, place__isnull=False).exclude(place='')     
        _args['age_' + _prefix_t]                    = _p
        _args['age_' + _prefix_t +'_estrada']        = return_list_filtered_by_form(_p.filter(nomination = 'estrada'), rnd_flag)
        _args['age_' + _prefix_t + '_narod']         = return_list_filtered_by_form(_p.filter(nomination = 'narod'), rnd_flag)
        _args['age_' + _prefix_t + '_narod_style']   = return_list_filtered_by_form(_p.filter(nomination = 'narod_style'), rnd_flag)
        _args['age_' + _prefix_t + '_sovremen_svobod']   = return_list_filtered_by_form(_p.filter(nomination = 'sovremen_svobod'), rnd_flag)
        _args['age_' + _prefix_t + '_sovremen_ulica']    = return_list_filtered_by_form(_p.filter(nomination = 'sovremen_ulica'), rnd_flag)
        _args['age_' + _prefix_t + '_spec']              = return_list_filtered_by_form(_p.filter(nomination = 'spec'), rnd_flag)
        return _args

def results(request):
    rnd_flag = 'results'
    args = {} 
    args['year'] = datetime.now().year

    # дети
    args.update(template_args_child('0-7', '0_7' , rnd_flag))
    args.update(template_args_child('8-10', '8_10', rnd_flag))
    
    # взрослые
    args.update(template_args_adults('11-14', '11_14', rnd_flag))
    args.update(template_args_adults('15-18', '15_18', rnd_flag))
    args.update(template_args_adults('18-25', '18_25', rnd_flag)) 
            
    #СМЕШАННАЯ================================
        
    # Смешанная кидс
    _p_kids = Participation.objects.filter(age_group='hybrid', category='kids' ) 
    args['age_hybrid_kids']  = _p_kids 
    args['age_hybrid_kids_estrada']         = return_list_filtered_by_form(_p_kids.filter(nomination = 'estrada'), rnd_flag)
    args['age_hybrid_kids_narod']           = return_list_filtered_by_form(_p_kids.filter(nomination = 'narod'), rnd_flag)
    args['age_hybrid_kids_narod_style']     = return_list_filtered_by_form(_p_kids.filter(nomination = 'narod_style'), rnd_flag)
    args['age_hybrid_kids_sovremen_svobod'] = return_list_filtered_by_form(_p_kids.filter(nomination = 'sovremen_svobod'), rnd_flag)
    args['age_hybrid_kids_sovremen_ulica']  = return_list_filtered_by_form(_p_kids.filter(nomination = 'sovremen_ulica'), rnd_flag)
    args['age_hybrid_kids_spec']            = return_list_filtered_by_form(_p_kids.filter(nomination = 'spec'), rnd_flag)
        
    # Смешанная взрослые
    _p_adults = Participation.objects.filter(age_group='hybrid', category='adults' )
    args['age_hybrid_adults']  = _p_adults
    args['age_hybrid_adults_estrada']           = return_list_filtered_by_form(_p_adults.filter(nomination = 'estrada'), rnd_flag)
    args['age_hybrid_adults_narod']             = return_list_filtered_by_form(_p_adults.filter(nomination = 'narod'), rnd_flag)
    args['age_hybrid_adults_narod_style']       = return_list_filtered_by_form(_p_adults.filter(nomination = 'narod_style'), rnd_flag)
    args['age_hybrid_adults_sovremen_svobod']   = return_list_filtered_by_form(_p_adults.filter(nomination = 'sovremen_svobod'), rnd_flag)
    args['age_hybrid_adults_sovremen_ulica']    = return_list_filtered_by_form(_p_adults.filter(nomination = 'sovremen_ulica'), rnd_flag)
    args['age_hybrid_adults_spec']              = return_list_filtered_by_form(_p_adults.filter(nomination = 'spec'), rnd_flag)

    # Смешанная , спец
    args['age_hybrid_spec'] = Participation.objects.filter(age_group='hybrid', category='spec' )

    return render(request, 'app/results.html', args
         #context_instance = RequestContext(request, args)
    )


class CommonView(TemplateView):
    """ 
    commmon class for views with date args an etc
    """
    template_name = 'app/index.html'
    #def __init__(self, **kwargs):        
    #    self.context = {}
    #    self.context['year'] = datetime.now().year
    def get_context_data(self, **kwargs):
        context = super(CommonView, self).get_context_data(**kwargs)
        context['year'] = datetime.now().year
        return context    

#фото-галерея
class FotoView(CommonView):
    
    template_name = 'app/foto_gallery.html'

    def get_context_data(self, **kwargs):
        context = super(FotoView, self).get_context_data(**kwargs)
        context['title'] = u'Фото-галлерея'  
        context['albums'] = Album.objects.all()       
        return context

class VideoView(CommonView):
    
    template_name = 'app/foto_gallery.html'

    def get_context_data(self, **kwargs):
        context = super(VideoView, self).get_context_data(**kwargs)
        context['title'] = u'Видео-галлерея'        
        return context

def reglament(request):
    """Renders the reglament page."""
    assert isinstance(request, HttpRequest)
    args = {
            'title': u'Положение',
            'message':'Your contact page.',
            'year': datetime.now().year,
    }

    return render( request, 'app/reglament.html',  args )

def news(request):
    args = {}
    #_news = News.objects.all().order_by('-date_creation')[:5]
    args['title'] = u'Новости'
    args['year'] = datetime.now().year
    args['news'] = News.objects.all().order_by('-date_creation') #[:5]
    return render(
        request,
        'app/news.html',
        args #context_instance = RequestContext(request, args )        
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    args = {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
    }

    return render( request, 'app/about.html', args )

def register_view(request):
    args = {}
    args.update(csrf(request))
    #args['form'] = UserCreationForm()
    args['form'] = UserRegistrationForm()
    args['title'] = u'Форма регистрации'
    args['year'] = datetime.now().year

    if request.POST:
        #newuser_form = UserCreationForm(request.POST) 
        newuser_form = UserRegistrationForm(request.POST) 
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username = newuser_form.cleaned_data['username'] , 
                                        password = newuser_form.cleaned_data['password2'])
             # сразу залогиниваемся под только что созданным акком
            auth.login(request , newuser)            
            # после создания логина , создадим соотвествующего Директора(Руководителя), к которому все привязано
            new_dir = Director()
            new_dir.user = auth.get_user(request)
            new_dir.date_change_dir  = datetime.now() 
            # после сохранения в базу , копируем адрес почты в таблицу Director
            new_dir.email = newuser_form.cleaned_data["email"]
            new_dir.save(); 
            messages.add_message(request, messages.SUCCESS, 'Аккаунт создан успешно')            

            #отправляем админам письмо о создании коллектива 
            _mails_admin = User.objects.filter(is_superuser = 1).values_list('email', flat=True)
            for mail in _mails_admin:
                try:
                    send_mail('Subject here', u'Зарегистрировался пользователь {0}'.format(new_dir.user),
                              'dance@radugafest.com', [mail], fail_silently=False)
                except Exception as ex:
                    print ex.message     
            
            # отправляем письмо самому юзеру об успешном создании логина и пароля
            message_for_user = u'Вы успешно зарегистрировались в личном кабинете Межданродного конкурса-фестиваля "Радуга-танца" \
                 г. Чебоксары. \n Ваши данные для входа: \n Логин: {0} \n Пароль: {1}  \n ссылка для входа в личный кабинет: http://cabinet.radugafest.com/login/'\
                 .format(newuser_form.cleaned_data['username'], newuser_form.cleaned_data['password2'])
            #_html_message = render_to_string('app/mail_after_registration.html', context)
            try:
                send_mail(u'Вы успешно зарегистрировались на сайте radugafest.com', message_for_user,
                              'dance@radugafest.com', [newuser_form.cleaned_data['email']], fail_silently=False, )
                              #html_message= _html_message)
            except Exception as ex:
                    print ex.message

            # после регистрации перенаправляем пользователя заполнять страницу профиля            
            #return redirect(reverse('editDir'))   # пока отменили эту функцию
            return redirect('/');       
        else:
            args['form'] = newuser_form
    return render_to_response('register.html' , args)

def test_view(request):
    args = {
            'title':'Сайт на реконструкции',            
            'year':datetime.now().year,
    }
    return render( request, 'test.html', args
        #context_instance = RequestContext(request,
        #{
        #    'title':'Сайт на реконструкции',            
        #    'year':datetime.now().year,
        #})
    ) 
#def Main_view(request):
def homeAng(request):   # Angular version
    args = {}

    _id = auth.get_user(request).id
    #args.update(csrf(request)) 
    args['title'] = u'Главная'    

    args['username'] = auth.get_user(request).username      
     
    # profile
    #_dir = Director.objects.get   ( user_id =_id )
    #_dir = serializers.serialize('json', [_member,], fields=('age_group','first_name',
    #                                                  'last_name','age', 'gender','status','status_comment'))
    try:
        _dir =  Director.objects.get( user_id =_id )
        args['directorOfGroup'] = serializers.serialize('json', [_dir,]) #, fields=('age_group','first_name',
                                                      #'last_name','age', 'gender','status','status_comment'))
    except ObjectDoesNotExist:
        args['directorOfGroup'] = " "
    return _json_response(args)

def home(request): 
        
    _user = auth.get_user(request)
    print '-----begin home----'
    if _user.is_superuser:
        return redirect('/admin')
    if not _user.is_authenticated():
        #return redirect('/login');
        print '-----redirect'
        return redirect(reverse('login'))
    else:
        _id = auth.get_user(request).id      # ИД авторизированного юзера
        
        # отменили пока проверку 2016.04.04
        ## проверяем заполено ли в профиле поле с e-mail и имя коллектива, если нет , отправляем заполнять
        #print "---mail is : -------"
        #print Director.objects.get(user_id = _id).email
        #if (Director.objects.get(user_id = _id).email in ['', None]) or \
        #    (Director.objects.get(user_id = _id).groupName in ['', None]): 
        #    return redirect(reverse('editDir'))

        args = {}
        args.update(csrf(request)) 
        args['title'] = u'Главная'    

        args['username'] = auth.get_user(request).username       
       # profile
        try:
            args['directorOfGroup'] =  Director.objects.get( user_id =_id )
        except ObjectDoesNotExist:
            args['directorOfGroup'] = " "
        # --news--
        try:
            args['news'] =  News.objects.order_by('id').reverse()[:3]      # берем только 3 последние новости 
        except ObjectDoesNotExist:
            args['news'] = " "
        #-- member--
        try:
            args['members'] = ( Member.objects.filter( user_id =_id ))        
        except ObjectDoesNotExist:
            args['members'] = " "
        # передаем экземпляр формы для добавления участника
        args['form'] = MemberForm() 

        # передаем форму для загрузки фотки
        args['formFoto'] = DirectorUploadFile()
        # передаем форму для редактирования профиля
        args['formEditDir'] = DirectorEditForm( instance = get_object_or_404(Director , user_id =_id))    #Director.objects.get(user_id =_id) )
    
        #--Particapation--
        try:
            args['participation'] = ( Participation.objects.filter( user_id =_id ))
        except ObjectDoesNotExist:
            args['participation'] = " "    
        args['formParticipation'] = ParticipationForm(_user = _id)
        #сумма оргвзноса за заявки на участие
        sumParticipation = 0
        for parton in Participation.objects.filter(user_id = _id):
            sumParticipation += parton.payment
        args['sumParticipation'] = sumParticipation
        #print "---print Participation================"
        #print sumParticipation
        #--Residing--
        try:
            args['residing'] = ( Residing.objects.filter( user_id =_id ))
        except ObjectDoesNotExist:
            args['residing'] = " "    
        args['formResiding'] = ResidingForm(_user = _id)    

        #--Transfer--
        try:
            args['transfers'] = ( Transfer.objects.filter( user_id =_id ))
        except ObjectDoesNotExist:
            args['transfers'] = " "
        args['formTransfer'] = TransferForm(_user = _id)  # передаем параметр для фильтрации место прибытия
        #--Excursion
        try:
            args['excursions'] = ( Excursion.objects.filter( user_id =_id ))
        except ObjectDoesNotExist:
            args['excursions'] = " "
        args['formExcursion'] = ExcursionForm(_user = _id)
        
        #--Food--
        try:
            args['foods'] = ( Food.objects.filter( user_id =_id ))
        except ObjectDoesNotExist:
            args['foods'] = " "    
        args['formFood'] = FoodForm(_user = _id)

        args['year']  = datetime.now().year                             
        
        #return render_to_response('Member_raduga_template.html'  ,  args , context_instance=RequestContext(request))      
        return render( request, 'Member_raduga_template.html', args )                
                #context_instance = RequestContext(request, args)  # old version render , prior 1.10 
            #)

def UploadFoto_view(request):   
    if request.POST:
        _id = auth.get_user(request).id
        Profile = Director.objects.get(user_id =_id)
        form = DirectorUploadFile(request.POST, request.FILES, instance=Profile)
        if form.is_valid():                    
            form.save()   
    else:
        form = DirectorUploadFile(instance=Profile)
        args ={}
        args['formFoto'] = form
        return render_to_response('Member_raduga_template.html' , args)
    return redirect('/');

def EditDir_view(request):    
    print '======edit Dir======'
    _id = auth.get_user(request).id 
    print _id   
    #_foto = Director.get(request).foto
    Profile = get_object_or_404(Director , user_id =_id )   
    print Profile
    args = {}
    if request.method == 'GET':
        if request.is_ajax():   # для главного окна
            response_data = serializers.serialize('json', [Profile,] ) #, 
                                                  #fields=('category','nomination','age_group','subgroup'))         
            print response_data
            return _json_response(response_data)  
        else:   # для страницы с отдельным 
            #DirectorEditForm( instance = get_object_or_404(Director , user_id =_id))         
            args['formEditDir'] = DirectorEditForm( instance=Profile )
            return render(
                request,
                'Profile_template.html',                
                args #context_instance = RequestContext(request, args)
            )
    if request.POST:       
        print request.POST
        formDir = DirectorEditForm( request.POST , instance=Profile )
        if formDir.is_valid():                                  
            dir = formDir.save(commit=False)   
            # сохраняем в базу с Большой буквы    
            dir.groupName       = formDir.cleaned_data['groupName'].title()  
            #dir.country         = formDir.cleaned_data['country'].title() 
            dir.city            = formDir.cleaned_data['city'].title()
            dir.director        = formDir.cleaned_data['director'].title()
            dir.teacher         = formDir.cleaned_data['teacher'].title()
            dir.institution         = formDir.cleaned_data['institution'].title()
            #dir.addressInstitution  = formDir.cleaned_data['addressInstitution'].title()
            #dir.postalAddress       = formDir.cleaned_data['postalAddress'].title()
            formDir.save()   
            messages.add_message(request, messages.SUCCESS, u'Информация обновлена')
            return HttpResponse('ok')
        else:                  
            return _form_errors(formDir)    
    print "delete--"
    return redirect('/');

def MemberFrame_view(request):
    # для iframe 
    if request.method == "GET":
        print "--simply GET----"
        args= {}
        #_user = auth.get_user(request)
        _id = auth.get_user(request).id      # ИД авторизированного юзера
        try:
            args['members'] = ( Member.objects.filter( user_id =_id ))        
        except ObjectDoesNotExist:
            args['members'] = " "
        # передаем экземпляр формы для добавления участника
        args['form'] = MemberForm()
        return render( request, 'tables/TableMembersChild.html', args
            #context_instance = RequestContext(request, args)
        )

def CreateOrEditMember_view(request , member_id=None):
    if (member_id == None or member_id == '999999'):
        _member = Member()
        _message = 'Участник добавлен успешно'
    else:
        #_member = get_object_or_404( Member ,  id = member_id )
        _member = Member.objects.get(id = member_id)
        _message = 'Информация об участнике обновлена успешно'
    if request.method == "GET" and request.is_ajax():        
        data = serializers.serialize('json', [_member,], fields=('age_group','first_name',
                                                      'last_name','age', 'gender','status','status_comment'))
        return _json_response(data)        
    
    if request.POST:
        response_data = {}  # словарь для JSON-ответа
        print request.POST 

        formMember = MemberForm(request.POST ,request.FILES, instance = _member )
        if formMember.is_valid():
            member = formMember.save(commit=False)
            member.user_id = auth.get_user(request).id   #передаем  ID директора , к которому привязан участник 
            # переписываем фамилию и имя с большой буквы            
            member.first_name       = formMember.cleaned_data['first_name'].title()
            member.last_name        = formMember.cleaned_data['last_name'].title()   
            # дата последнего редактирования самим руководителем
            member.date_change_dir  = datetime.now()         
            formMember.save()
            #messages.add_message(request, messages.SUCCESS, _message)   
            return HttpResponse('ok')
        else:
            #_message = u'Неправильно заполнена форма'
            #messages.add_message(request, messages.ERROR, _message)   
            response_data['errors']     = u'Неправильно заполнена форма'
            response_data['formErrors'] = simplejson.dumps(formMember.errors)            
            return _json_response(response_data)
    else:
        args = {}
        args.update(csrf(request))         
        args['form'] = MemberForm(instance = _member)
        args['user_id'] = auth.get_user(request).id        
        return render_to_response('Create_member.html', args)
    #return redirect(reverse('Main'));
    return redirect('/');

def DeleteMember_view(request , member_id):    
    if request.POST:        
        Member.objects.get( id = member_id ).delete()   
        #messages.add_message(request, messages.SUCCESS, u"Информация об участнике удалена.")        
    #return redirect(reverse('home'));     
    return HttpResponse('ok')    

#Participation-----------------------------------------------------------------------
def ParticipationFrame_view(request):
    # для iframe 
    if request.method == "GET":
        print "--simply GET----"
        args= {}
        #_user = auth.get_user(request)
        _id = auth.get_user(request).id      # ИД авторизированного юзера
        try:
            args['participation'] = ( Participation.objects.filter( user_id =_id ))
        except ObjectDoesNotExist:
            args['participation'] = " "    
        args['formParticipation'] = ParticipationForm(_user = _id)
        #сумма оргвзноса за заявки на участие
        sumParticipation = 0
        for parton in Participation.objects.filter(user_id = _id):
            sumParticipation += parton.payment
        args['sumParticipation'] = sumParticipation
        return render( request, 'tables/TableParticipationsChild.html', args
            #context_instance = RequestContext(request, args)
        )

@csrf_protect
def CreateOrEditParticipation_view(request , participation_id=None):
    if (participation_id == None or participation_id == '999999'):        
        _participation = Participation()
        _message = 'Заявка добавлена успешно'

        ## заявки закрыли для добавления , по условиям конкурса
        #_message = 'Добавление заявок прекращено'
        #messages.add_message(request, messages.SUCCESS, _message) 
        #return redirect('/');
    else:
        _participation = get_object_or_404( Participation ,  id = participation_id )
        _message = 'Заявка отредактирована успешно'
    if request.method == "GET" and request.is_ajax():        
        #response_data = {}        
        response_data = serializers.serialize('json', [_participation,], fields=(
                                        'category','nomination','age_group','subgroup',
                                        'form_of_execution','list_member', 'member1','member2','member3',
                                        'composition_1',
                                        'description_comp', 'status','status_comment', 'payment'))         
        return _json_response(response_data)        

    if request.POST:   
        response_data = {}  # словарь для JSON-ответа
        print request.POST           
        formParticipation = ParticipationForm(request.POST , request.FILES, instance = _participation ) # , _user = auth.get_user(request).id )        
        if formParticipation.is_valid():            
            parton = formParticipation.save(commit=False)
            parton.user_id = auth.get_user(request).id   #передаем  ID директора , к которому привязан участник 
            parton.status = 'moderacia'
            parton.payment = 0 # УБРАТЬ , когда запустим функцию подсчета , Проверить надо ли убирать
            parton.date_change_dir  = datetime.now()            
            # Если участник использует чекбокс "Свое название", то сохраняем его в базу            
            if ('subgroupSelf' in request.POST) and \
                request.POST['subgroupSelf'] not in \
                list(Subgroup_choices.objects.filter(user_id = auth.get_user(request)).values_list('subgroup_name',\
                    flat=True)):                   
                    newSubgroup = Subgroup_choices(
                        user = auth.get_user(request),
                        subgroup_name =  request.POST['subgroupSelf'] 
                    )
                    newSubgroup.save()
                    parton.subgroup =  newSubgroup 
        
            # флаг , если pk = None значит заявка новая и пишем в письме "создал" иначе , отредактировал
            flag_new_request = True if parton.pk is None else False 
        
            #отправляем письмо в санаторий о размещении , ящик находим в таблице Mails
            _mails = list(Mails.objects.filter(app_type = 'participation' ).values_list('mail', flat=True))
            print _mails        
            print '--------1111 in View Participation ----'
            # рассылка санаториям о добавлении заявки
            context = {
                'flag_new_request'  : flag_new_request,
                'req_parton'        : parton,
                'dir'               : Director.objects.get(user_id = parton.user),   #self.user),                    
            }        
            print Director.objects.get(user_id = parton.user).user.username
            html = render_to_string('app/parton_for_mail.html', context)        
            try:            
                send_mail('Заявка на участие. "Радуга-танца" г.Чебоксары' , u'Заявка от {0}'.format(parton.user),
                            'dance@radugafest.com', _mails , fail_silently=False,
                            html_message=html)
            except Exception as ex:
                print 'exception mail'
                print ex  #print ex.message

            formParticipation.save()    
            _count_member = request.POST['list_member'] if request.POST['list_member'] else 0  #len(request.POST.getlist('list_member')) 
            # отключили 2016.04.18 - решили считать вручную 
            # перенес в модель , вызывается при сохранении заявки
            Calc(instance=_participation , kwargs = {'count' : _count_member} )      
            #messages.add_message(request, messages.SUCCESS, _message) 
            return HttpResponse('ok') 
              
        else:                     
            response_data['errors']     = u'Неправильно заполнена форма.' 
            response_data['formErrors'] = simplejson.dumps(formParticipation.errors)
            return _json_response(response_data)

    return redirect('/');    

       
                    
def DeleteParticipation_view(request , participation_id):    
    if request.POST:        
        Participation.objects.get( id = participation_id ).delete()   
        #messages.add_message(request, messages.SUCCESS, u"Заявка удалена.")        
    return HttpResponse('ok')
    #return redirect('/');

#Residing
def ResidingFrame_view(request):
    # для iframe 
    if request.method == "GET":
        print "--simply GET----"
        args= {}
        #_user = auth.get_user(request)
        _id = auth.get_user(request).id      # ИД авторизированного юзера
        try:
            args['residing'] = ( Residing.objects.filter( user_id =_id ))
        except ObjectDoesNotExist:
            args['residing'] = " "    
        args['formResiding'] = ResidingForm(_user = _id)   # передаем параметр для фильтрации ? место прибытия
        return render( request, 'tables/TableResidingsChild.html', args
            #context_instance = RequestContext(request, args)
        )
def CreateOrEditResiding_view(request , residing_id=None):
    response_data = {} # словарь для JSON-ответа
    if (residing_id == None or residing_id == '999999'):        
        _residing = Residing()
        _message = 'Заявка добавлена успешно'
    else:
        _residing = get_object_or_404( Residing ,  id = residing_id )        
        _message = 'Заявка отредактирована успешно'
    if request.method == "GET" and request.is_ajax():       
        # сериализуем только queryset поэтому заворчаиваем объект в [obj,]
        data = serializers.serialize('json', [_residing,], fields=('place_of_residing','quantity_total','quantity_adult_male',
                'quantity_adult_female', 'quantity_member_male', 'quantity_member_female', 
                'date_arrival','time_arrival','date_departure','time_departure','status','status_comment'))
        return _json_response(data) 

    if request.POST:        
        formResiding = ResidingForm(request.POST , instance = _residing )
        if formResiding.is_valid():
            res = formResiding.save(commit=False)
            res.user_id = auth.get_user(request).id   #передаем  ID директора , к которому привязан участник 
            # Рассчитываем сумму заявки и сохраняем ;           
            res.payment =  fee_residing
            messages.add_message(request, messages.SUCCESS, _message)  
            formResiding.save()  
            return HttpResponse('ok')
        else:
            response_data['errors']     = u'Неправильно заполнена форма.'
            response_data['formErrors'] = simplejson.dumps(formResiding.errors)
            return _json_response(response_data)                
    return redirect('/');
def DeleteResiding_view(request , residing_id):    
    if request.POST:        
        Residing.objects.get( id = residing_id ).delete()    
        messages.add_message(request, messages.SUCCESS, "Заявка удалена")       
    return HttpResponse('ok')
    #return redirect('/');

#Transfer
def TransferFrame_view(request):
    # для iframe 
    if request.method == "GET":
        print "--simply GET----"
        args= {}
        #_user = auth.get_user(request)
        _id = auth.get_user(request).id      # ИД авторизированного юзера
        try:
            args['transfers'] = ( Transfer.objects.filter( user_id =_id ))
        except ObjectDoesNotExist:
            args['transfers'] = " "
        args['formTransfer'] = TransferForm(_user = _id)  # передаем параметр для фильтрации место прибытия
        return render( request, 'tables/TableTransfersChild.html', args
            #context_instance = RequestContext(request, args)
        )
def CreateOrEditTransfer_view(request , transfer_id=None):
    response_data = {} # словарь для JSON-ответа
    if (transfer_id == None or transfer_id == '999999'):        
        _transfer = Transfer()
        _message = 'Заявка добавлена успешно'        
    else:
        _transfer = get_object_or_404( Transfer ,  id = transfer_id )
        _message = 'Заявка отредактирована успешно'
    if request.method == "GET" and request.is_ajax():       
        # сериализуем только queryset поэтому заворчаиваем объект в [obj,]
        data = serializers.serialize('json', [_transfer,], fields=('date_departure', 'time_departure', 'place_departure',
                'place_arrival', 'quantity_total', 'quantity_adult', 'quantity_member',
                'status','status_comment'))
        return _json_response(data) 
    if request.POST:            
        formTransfer = TransferForm(request.POST , instance = _transfer )
        if formTransfer.is_valid():            
            res = formTransfer.save(commit=False)
            res.user_id = auth.get_user(request).id   #передаем  ID директора , к которому привязан участник           
                        
            # Если участник использует чекбокс "Свое название", то сохраняем его в базу             
            if ('transDepartureSelf' in request.POST) and \
                request.POST['transDepartureSelf'] not in \
                list(Place_departure_choices.objects.filter(user_id = auth.get_user(request)).values_list('place_name',\
                    flat=True)):                   
                    new_dep_place = Place_departure_choices(
                        user = auth.get_user(request),
                        place_name = request.POST['transDepartureSelf'] 
                    )
                    new_dep_place.save()
                    res.place_departure =  new_dep_place
            
            if ('transArrivalSelf' in request.POST) and \
                request.POST['transArrivalSelf'] not in \
                list(Place_departure_choices.objects.filter(user_id = auth.get_user(request)).values_list('place_name',\
                    flat=True)):                   
                        new_arriv_place = Place_departure_choices(
                            user = auth.get_user(request),
                            place_name = request.POST['transArrivalSelf'] 
                        )
                        new_arriv_place.save()
                        res.place_arrival =  new_arriv_place
            
            # Рассчитываем сумму заявки и сохраняем ;
            res.payment =  fee_transfer

            formTransfer.save()  
            messages.add_message(request, messages.SUCCESS, _message)
            return HttpResponse('ok')
        else:
            response_data['errors']     = u'Неправильно заполнена форма.' 
            response_data['formErrors'] = simplejson.dumps(formTransfer.errors)
            return _json_response(response_data)
    return redirect('/');
def DeleteTransfer_view(request , transfer_id):    
    if request.POST:        
        Transfer.objects.get( id = transfer_id ).delete()    
        #messages.add_message(request, messages.SUCCESS, "Заявка удалена")       
    return HttpResponse('ok')
    #return redirect('/');

#Excursion
def ExcursionFrame_view(request):
    # для iframe 
    if request.method == "GET":
        print "--simply GET----"
        args= {}
        #_user = auth.get_user(request)
        _id = auth.get_user(request).id      # ИД авторизированного юзера
        try:
            args['excursions'] = ( Excursion.objects.filter( user_id =_id ))
        except ObjectDoesNotExist:
            args['excursions'] = " "
        args['formExcursion'] = ExcursionForm(_user = _id)
        return render( request, 'tables/TableExcursionsChild.html', args
                 #context_instance = RequestContext(request, args)
        )
def CreateOrEditExcursion_view(request , excursion_id=None):
    response_data = {} # словарь для JSON-ответа
    if (excursion_id == None or excursion_id == '999999'):        
        _excursion = Excursion()
        _message = 'Заявка добавлена успешно'
    else:
        _excursion = get_object_or_404( Excursion ,  id = excursion_id )
        _message = 'Заявка отредактирована успешно'
    if request.method == "GET" and request.is_ajax():       
        # сериализуем только queryset поэтому заворчаиваем объект в [obj,]
        data = serializers.serialize('json', [_excursion,], fields=('tour_form','date_departure', 'time_departure', 'place_departure',
                'place_arrival', 'quantity_total', 'quantity_adult', 'quantity_member',
                'status','status_comment'))
        return _json_response(data) 
    if request.POST:        
        print request.POST
        formExcursion = ExcursionForm(request.POST , instance = _excursion )
        if formExcursion.is_valid():
            res = formExcursion.save(commit=False)
            print res
            print "---after res---"
            res.user_id = auth.get_user(request).id   #передаем  ID директора , к которому привязан участник 
            
            if ('exDepartureSelf' in request.POST): #and \
                # удаляем остатки , если в форме сохранился предыдущий вариант
                #request.POST.pop('place_departure')
                if request.POST['exDepartureSelf'] not in \
                    list(Place_departure_choices.objects.filter(user_id = auth.get_user(request)).values_list('place_name',\
                        flat=True)):                   
                        new_dep_place = Place_departure_choices(
                            user = auth.get_user(request),
                            place_name = request.POST['exDepartureSelf'] 
                        )
                        new_dep_place.save()
                        res.place_departure =  new_dep_place
                        # если места прибытие и отбытие равно , то приверяем здесь и схраняем
                        #if (request.POST['exDepartureSelf'] == request.POST['exArrivalSelf'] ):
                        #    res.place_arrival = new_dep_place
                # если такой выбор уже был , то сохраняем его , если так не делать то сохраняется None
                else:
                    new_dep_place = Place_departure_choices.objects.get(user_id=auth.get_user(request).id, 
                                                                           place_name = request.POST['exDepartureSelf'])
                    res.place_departure =  new_dep_place

            if ('exArrivalSelf' in request.POST):  #and \
                # удаляем остатки , если в форме сохранился предыдущий вариант
                #request.POST.pop('place_arrival')
                if request.POST['exArrivalSelf'] not in \
                    list(Place_departure_choices.objects.filter(user_id = auth.get_user(request)).values_list('place_name',\
                        flat=True)):                   
                        # сохраняем новое место только если оно не равно отбытию , которое уже сохранили выше
                        if (request.POST['exDepartureSelf'] != request.POST['exArrivalSelf'] ):                        
                            new_arriv_place = Place_departure_choices(
                                user = auth.get_user(request),
                                place_name = request.POST['exArrivalSelf'] 
                            )
                            new_arriv_place.save()
                            res.place_arrival =  new_arriv_place
                else:                    
                    new_arriv_place = Place_departure_choices.objects.get(user_id=auth.get_user(request).id, 
                                                                           place_name = request.POST['exDepartureSelf'])
                    res.place_arrival =  new_arriv_place

            # Рассчитываем сумму заявки и сохраняем ;
            res.payment =  fee_excursion

            messages.add_message(request, messages.SUCCESS, _message)  
            formExcursion.save()  
            return HttpResponse('ok')
        else:
            response_data['errors']     = u'Неправильно заполнена форма.' 
            response_data['formErrors'] = simplejson.dumps(formExcursion.errors)
            return _json_response(response_data)
    return redirect('/');
def DeleteExcursion_view(request , excursion_id):    
    if request.POST:        
        Excursion.objects.get( id = excursion_id ).delete()    
        #messages.add_message(request, messages.SUCCESS, "Заявка удалена")       
    #return redirect('/');
    return HttpResponse('ok')

#Food
def FoodFrame_view(request):
    # для iframe 
    if request.method == "GET":        
        args= {}
        #_user = auth.get_user(request)
        _id = auth.get_user(request).id      # ИД авторизированного юзера
        try:
            args['foods'] = ( Food.objects.filter( user_id =_id ))
        except ObjectDoesNotExist:
            args['foods'] = " "    
        args['formFood'] = FoodForm(_user = _id)   # передаем параметр (осталось от проживания)
        return render( request, 'tables/TableFoodsChild.html', args )

def CreateOrEditFood_view(request , food_id=None):
    response_data = {} # словарь для JSON-ответа
    if (food_id == None or food_id == '999999'):        
        _food = Food()
        _message = 'Заявка добавлена успешно'
    else:
        _food = get_object_or_404( Food ,  id = food_id )        
        _message = 'Заявка отредактирована успешно'
    if request.method == "GET" and request.is_ajax():       
        # сериализуем только queryset поэтому заворчаиваем объект в [obj,]
        data = serializers.serialize('json', [_food,], )#fields=('place_of_residing','quantity_total','quantity_adult',
                #'quantity_member', 'date','status','status_comment'))
        return _json_response(data) 

    if request.POST:        
        print request.POST
        formFood = FoodForm(request.POST , instance = _food )
        if formFood.is_valid():
            res = formFood.save(commit=False)
            res.user_id = auth.get_user(request).id   #передаем  ID директора , к которому привязан участник 
            print res.zavtrak
            print res.obed
            print res.ugin
            res.zavtrak = 1 if ('zavtrak' in request.POST) else 0
            res.obed = 1 if ('obed' in request.POST) else 0
            res.ugin = 1 if ('ugin' in request.POST) else 0
            print res.zavtrak
            print res.obed
            print res.ugin
            # Рассчитываем сумму заявки и сохраняем ;           
            #res.payment =  fee_food
            #messages.add_message(request, messages.SUCCESS, _message)  
            formFood.save()  
            return HttpResponse('ok')
        else:
            response_data['errors']     = u'Неправильно заполнена форма.'
            response_data['formErrors'] = simplejson.dumps(formFood.errors)
            return _json_response(response_data)                
    return redirect('/');
def DeleteFood_view(request , food_id):    
    if request.POST:        
        Food.objects.get( id = food_id ).delete()    
        messages.add_message(request, messages.SUCCESS, "Заявка удалена")       
    return HttpResponse('ok')