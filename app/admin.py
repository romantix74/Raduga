# -*- coding: utf-8 -*-
#created 17.08.2015 by myself

from django.contrib import admin 
from django.contrib.admin import AdminSite

from models import Member, Country, Director, News, Reglaments, Participation, \
                    Place_residing_choices, Residing, Transfer, \
                    Tours, Excursion , Place_departure_choices, \
                    Subgroup_choices, Mails , Album, Foto, Video

from sorl.thumbnail.admin import AdminImageMixin
# regiter group of Memeber in admin site (adminka)
#admin.site.register(Member)  

# рендеринга свей страницы с Графиками выступлений 2016.03.28
from django.shortcuts import render, render_to_response, redirect , get_object_or_404
from django.conf.urls import url

from datetime import datetime
from django.contrib import auth
from django.core.mail import send_mail

from django.contrib.admin import SimpleListFilter

from django.http.response import HttpResponse

import os
from os import path

from engine.admin_engine import generate_diplom , _cp_music
from engine.calc import Calc

#для мультизагрузки фоток в галлерею
from widgets import MultiFileInput
from django import forms
from django.utils.encoding import smart_str

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.conf import settings


#PROJECT_ROOT = path.dirname(path.abspath(path.dirname(__file__)))

# отдельные регистры , так как их не надо аппрувить 
#class MemberInline(admin.TabularInline):
#    model = Member
#class DirectorAdmin(admin.ModelAdmin):
#    inlines = [
#        MemberInline,
#    ]
#admin.site.register(Director, DirectorAdmin) 

# Страна
admin.site.register(Country)

class DirectorAdmin(admin.ModelAdmin):
    list_display = ['groupName', 'fullAddress', 'director', 'teacher']
admin.site.register(Director, DirectorAdmin)
#admin.site.register(Director)

# при добавлении новости отправляем на почту эту новость , желательно еще прикрутить веб-редактор
class NewsAdmin(admin.ModelAdmin):
    pass
    #def save_model(self, request, obj, form, change):        
    #    # создаем список из почтовых ящиков всех руководителей
    #    mail_list_for_director = Director.objects.all().values_list('email', flat=True)
    #    for mail in mail_list_for_director:
    #        try:
    #            send_mail(u'Subject here', u'{0} , {1}'.format('body', str(obj.news)) , 'dance@radugafest.com',
    #                [mail], fail_silently=False)
    #        except Exception as ex:
    #            print ex.message
    #    obj.save()
admin.site.register(News, NewsAdmin)

# Положение
admin.site.register(Reglaments)

def make_approved(modeladmin, request, queryset):
    queryset.update(status='ok')
    queryset.update(date_change_admin=datetime.now())
make_approved.short_description = u"Пометить выбранных участников как 'Одобренные'"

# list общий для всех классов
common_list_display  = ['user', 'status', 'status_comment']

class CommonClass(AdminImageMixin, admin.ModelAdmin):
    actions = [make_approved]
    # для фильтрации по рукводителю
    list_filter = ['user__groupName']
    # поиск по коллективам
    search_fields = ['user__groupName']
        
##@admin.register(Member) 
#class MemberAdmin(AdminImageMixin, admin.ModelAdmin):
class MemberAdmin(CommonClass):    
    list_display =  ['display_groupName' ,'age_group', 'first_name', 'last_name',
                                          'age', 'gender', 'scan_passport', ] + common_list_display
    #для формы
    fields        = ('user', 'age_group', 'first_name', 'last_name', 
                     'age', 'scan_passport', 'status', 'status_comment')
    #fields = list_display   
admin.site.register(Member, MemberAdmin)

#Participation
# функция рандомит внутри формы исполнения и затем сортирует в порядке - соло, дуэт, ансамбль
def filter_by_form(_qset):
    _res = []
    _res_solo = _qset.filter(form_of_execution='solo').order_by('?')
    _res_duet = _qset.filter(form_of_execution='duet').order_by('?')
    _res_ensamble = _qset.filter(form_of_execution='ensamble').order_by('?')
    for i in _res_solo:
        _res.append(i)
    for i in _res_duet:
        _res.append(i)
    for i in _res_ensamble:
        _res.append(i)
    return _res

_f_ex = ['solo', 'duet', 'ensamble']
def return_list_filtered_by_form(_qset, rnd_flag=False):
    CASE_SQL_PLACE = u'(case when place="1Л" then 1 \
                        when place="2Л" then 2 \
                        when place="3Л" then 3 \
                        when place="1Д" then 4 \
                        when place="2Д" then 5 \
                        when place="3Д" then 6 \
                        else 9999 \
                        end)' 
    _list_parton = []  # делаю дист и последовательно по форме : соло-дуэт-анс добавляю сюда parton-ы
    for fex in _f_ex:        
        if rnd_flag == True:            
            _list_parton.append(_qset.filter(form_of_execution=fex).order_by('?'))
        elif (rnd_flag == 'results'):           
            _list_parton.append(_qset.filter(form_of_execution=fex).\
                extra(select={'f_place': CASE_SQL_PLACE}, order_by=['f_place']) )
        else :
            _list_parton.append(_qset.filter(form_of_execution=fex) ) 
    return _list_parton

class ParticipationAdmin(CommonClass):   
    #class Media:
    #    css = {
    #        "all": ("admin_css.css",)
    #    }
    #    js = ("admin_js.js",)   
    #list_display = common_list_display + [ 'category', 'nomination', 'age_group', 'subgroup', 'form_of_execution', 
    #                                      'list_member_show', 'list_member_count', 'list_member_male_count', 
    #                                      'list_member_female_count',
    #                                      'composition_1', 'description_comp', ]   
    list_display = common_list_display + [ 'city_show', 'category', 'nomination', 'age_group',
                                          'subgroup', 'form_of_execution', 'list_member', 
                                          'member1', 'member2', 'member3',                                         
                                          'composition_1', 'description_comp', 'file_music',
                                          'payment', 'place']  
    #для формы
    fields =   common_list_display + [ 'category', 'nomination', 'age_group', 'subgroup', 'form_of_execution', 
                                      'list_member','member1', 'member2', 'member3', 
                                        'composition_1', 'description_comp', 'payment', 'place' ]  
    list_filter = ['user__groupName', 'nomination', 'age_group' , 'form_of_execution']  
    
    def get_urls(self):
        urls = super(ParticipationAdmin, self).get_urls()        
        my_urls = [
        #urls += [
            url(r'^grafic/$', self.admin_site.admin_view(self._admin_grafic), name='admin_grafic',), # графики выступлений            
            #url(r'^grafic_random/$', self.admin_site.admin_view(self._admin_grafic_random), {'rnd_flag': True}, #'random' - флаг для рандома внутри категории 
            #    name='admin_grafic_random', ), # графики выступлений рандом 
            url(r'^grafic_random/$', self.admin_site.admin_view(self._admin_grafic), {'rnd_flag': True}, #'random' - флаг для рандома внутри категории 
                name='admin_grafic_random', ), # графики выступлений рандом  
            url(r'^generate_place/$', self.admin_site.admin_view(self._generate_place), name='generate_place',), # графики выступлений      
            #url(r'^results/$', self.admin_site.admin_view(self._results),  {'rnd_flag': 'results'}, name='results',), # результаты вписываются сюда  
            url(r'^results/$', self.admin_site.admin_view(self._results), name='results',), # результаты вписываются сюда  
            # для обновления места
            #url(r'^place/(?P<participation_id>[0-9]+)-(?P<place>[0-9]+)/$',
            url(r'^place/$', self.admin_site.admin_view(self._place), name='place'),  
            url(r'^cp_music/$', self.admin_site.admin_view(self._cp_music_view), name='cp_music'),               
        ]        
        return my_urls + urls
        #return urls
    
    # сортировка по префиксу; добавляем элементы с заданными ключами и вычисленнными сетами    
    def template_args_child(self, _age_prefix , _prefix_t , rnd_flag = False):
        _nom_list = ['estrada', 'narod+_narod_style', 'suget_igrovoi', 'spec']         
        _return_dict = {} # словарь из листов для перебора в шаблоне

        _args = {}        # хранение переменных для шаблона    
        _p = Participation.objects.filter(age_group=_age_prefix)  
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

    def template_args_adults(self, _age_prefix , _prefix_t, rnd_flag = False):  # в шаблоне нельзя использовать знак "-" поэтому указываю сам префикс
        _args = {}      
        
        _p = Participation.objects.filter(age_group=_age_prefix)          
        
        _args['age_' + _prefix_t]                    = _p
        _args['age_' + _prefix_t +'_estrada']        = return_list_filtered_by_form(_p.filter(nomination = 'estrada'), rnd_flag)
        _args['age_' + _prefix_t + '_narod']         = return_list_filtered_by_form(_p.filter(nomination = 'narod'), rnd_flag)
        _args['age_' + _prefix_t + '_narod_style']   = return_list_filtered_by_form(_p.filter(nomination = 'narod_style'), rnd_flag)
        _args['age_' + _prefix_t + '_sovremen_svobod']   = return_list_filtered_by_form(_p.filter(nomination = 'sovremen_svobod'), rnd_flag)
        _args['age_' + _prefix_t + '_sovremen_ulica']    = return_list_filtered_by_form(_p.filter(nomination = 'sovremen_ulica'), rnd_flag)
        _args['age_' + _prefix_t + '_spec']              = return_list_filtered_by_form(_p.filter(nomination = 'spec'), rnd_flag)
        
        return _args

    def _admin_grafic(self, request, rnd_flag=False):
        print rnd_flag
        print "===after foo======"
        args = {} 
        args['opts'] = self.model._meta # для навигации наверху страницы
        # дети
        args.update(self.template_args_child('0-7', '0_7' , rnd_flag))
        args.update(self.template_args_child('8-10', '8_10', rnd_flag))
        # взрослые
        args.update(self.template_args_adults('11-14', '11_14', rnd_flag))
        args.update(self.template_args_adults('15-18', '15_18', rnd_flag))
        args.update(self.template_args_adults('18-25', '18_25', rnd_flag))  
        
        #СМЕШАННАЯ================================        
        # Смешанная кидс
        _p_kids = Participation.objects.filter(age_group='hybrid', category='kids' )
        args['age_hybrid_kids']  = _p_kids
        args['age_hybrid_kids_estrada']         = return_list_filtered_by_form(_p_kids.filter(nomination = 'estrada'), rnd_flag)
        args['age_hybrid_kids_narod']           = return_list_filtered_by_form(_p_kids.filter(nomination__contains='narod'), rnd_flag)
        args['age_hybrid_kids_suget'] = return_list_filtered_by_form(_p_kids.filter(nomination = 'suget-igrovoi'), rnd_flag)
        #args['age_hybrid_kids_spec']  = return_list_filtered_by_form(_p_kids.filter(nomination = 'spec'), rnd_flag)        
        
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
            #args['age_hybrid_spec'] = args['age_hybrid_adults'].filter(nomination = 'spec')

        return render_to_response('admin/app/change_list_grafic.html', args)
        #pass
    def _admin_grafic_random(self, request, rnd_flag=False):
        args = {} 
        args['opts'] = self.model._meta # для навигации наверху страницы
        # дети
        args.update(self.template_args_child('0-7', '0_7'))
        args.update(self.template_args_child('8-10', '8_10'))
        print args
        print "====after child 0 -7"

        # взрослые
        args.update(self.template_args_adults('11-14', '11_14'))
        args.update(self.template_args_adults('15-18', '15_18'))
        args.update(self.template_args_adults('18-25', '18_25'))  
        
        #СМЕШАННАЯ================================
        # Смешанная кидс
        args['age_hybrid_kids']  = Participation.objects.filter(age_group='hybrid', category='kids' )
        args['age_hybrid_kids_estrada']         = args['age_hybrid_kids'].filter(nomination = 'estrada')
        args['age_hybrid_kids_narod']           = args['age_hybrid_kids'].filter(nomination = 'narod')
        args['age_hybrid_kids_narod_style']     = args['age_hybrid_kids'].filter(nomination = 'narod_style')
        args['age_hybrid_kids_sovremen_svobod'] = args['age_hybrid_kids'].filter(nomination = 'sovremen_svobod')
        args['age_hybrid_kids_sovremen_ulica']  = args['age_hybrid_kids'].filter(nomination = 'sovremen_ulica')
        args['age_hybrid_kids_spec']            = args['age_hybrid_kids'].filter(nomination = 'spec')
        
        # Смешанная взрослые
        args['age_hybrid_adults']  = Participation.objects.filter(age_group='hybrid', category='adults' )
        args['age_hybrid_adults_estrada']           = args['age_hybrid_kids'].filter(nomination = 'estrada')
        args['age_hybrid_adults_narod']             = args['age_hybrid_adults'].filter(nomination = 'narod')
        args['age_hybrid_adults_narod_style']       = args['age_hybrid_adults'].filter(nomination = 'narod_style')
        args['age_hybrid_adults_sovremen_svobod']   = args['age_hybrid_adults'].filter(nomination = 'sovremen_svobod')
        args['age_hybrid_adults_sovremen_ulica']    = args['age_hybrid_adults'].filter(nomination = 'sovremen_ulica')
        args['age_hybrid_adults_spec']              = args['age_hybrid_adults'].filter(nomination = 'spec')

        # Смешанная , спец
        args['age_hybrid_spec'] = Participation.objects.filter(age_group='hybrid', category='spec' )
        #args['age_hybrid_spec'] = args['age_hybrid_adults'].filter(nomination = 'spec')

        return render_to_response('admin/app/change_list_grafic_random.html', args)

    # для создания изображений дипломов
    def _generate_place(self, request):
        if request.POST:
            #print request.POST
            _ps = Participation.objects.all()  #filter(place__isnull=False )
            for i,_p in enumerate(_ps):
                generate_diplom(_p, i)
            return HttpResponse('ok')
        return redirect('/');        
    
    def _place(self, request):  #, participation_id=None, place=None):     
        print request
        _participation_id = request.POST['participation_id'] 
        _place = request.POST['place'] 
        parton = Participation.objects.get(pk = _participation_id)
        parton.place = _place
        parton.save()
        return HttpResponse('ok')

    # для копирования музыки по номинациям
    def _cp_music_view(self, request):
        if request.POST:            
            _ps = Participation.objects.all()  #filter(place__isnull=False )
            _cp_music(_ps)
            return HttpResponse('ok')
        return redirect('/');

    def save_model(self, request, obj, form, change):
        print obj.user_id
        print obj.user
        print '---after user_id---'
        obj.save()  # вызываем перед переобсчетом , так как сам объект не переобновляется в этом методе и калк затирается
        #for p in Participation.objects.filter(user = obj.user_id):
        Calc( Participation.objects.filter(user = obj.user_id).first() ) # вызываем переобсчет заявок

    def _results(self, request): 
        rnd_flag = 'results'        
        args = {} 
        args['opts'] = self.model._meta # для навигации наверху страницы
        # дети
        args.update(self.template_args_child('0-7', '0_7' , rnd_flag))
        args.update(self.template_args_child('8-10', '8_10', rnd_flag))
        # взрослые
        args.update(self.template_args_adults('11-14', '11_14', rnd_flag))
        args.update(self.template_args_adults('15-18', '15_18', rnd_flag))
        args.update(self.template_args_adults('18-25', '18_25', rnd_flag))  
        
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
        #args['age_hybrid_spec'] = args['age_hybrid_adults'].filter(nomination = 'spec')  

        return render_to_response('admin/app/change_list_results.html', args)
        
admin.site.register(Participation, ParticipationAdmin)
 

#Заявки на участие отфильтрованные
#class ParticipationNominationAdmin(CommonClass):      
#    list_display =  [ 'collective_show','category', 'nomination', 'age_group' ]   
#    #для формы
#    fields =   common_list_display + [ 'category', 'nomination', 'age_group', 'subgroup', 'form_of_execution', 'list_member',
#                    'composition_1', 'description_comp', ]    
#admin.site.register(Participation, ParticipationNominationAdmin)

# Санатории проживания
admin.site.register(Place_residing_choices)

class ResidingAdmin(CommonClass):      
    list_display = common_list_display + [ 'mail_show', 'place_of_residing', 
                                        'quantity_total', 'quantity_adult_male', 'quantity_adult_female',
                                        'quantity_member_male', 'quantity_member_female', 'date_arrival', 'time_arrival',
                                        'date_departure', 'time_departure']   
    fields = list_display    
admin.site.register(Residing, ResidingAdmin)

class TransferAdmin(CommonClass):
    list_display = common_list_display + ['date_departure', 'time_departure', 'place_departure', 'place_arrival',
                                          'quantity_total', 'quantity_adult', 'quantity_member' ]
    fields = list_display    
admin.site.register(Transfer, TransferAdmin)


class ExcursionAdmin(CommonClass):      
    list_display = common_list_display + ['tour_form', 'date_departure', 'time_departure', 'place_departure', 'place_arrival',
                                          'quantity_total', 'quantity_adult', 'quantity_member']
admin.site.register(Excursion, ExcursionAdmin)

# настройка почты для разного типа заявок
admin.site.register(Mails)

#фото-галлерея
class FotoAdminForm(forms.ModelForm):
    class Meta:
        model = Foto
        widgets = {'image':MultiFileInput}
        fields = ['album', 'title', 'image']
class FotoAdmin(admin.ModelAdmin):
    form = FotoAdminForm
    list_filter = ['album']    # сортировка по названию альбома

    def add_view(self, request, *args, **kwargs):
        images = request.FILES.getlist('image',[])
        is_valid = FotoAdminForm(request.POST, request.FILES).is_valid()
 
        if request.method == 'GET' or len(images)<=1 or not is_valid:
            return super(FotoAdmin, self).add_view(request, *args, **kwargs)
        # если фоток , больше одной , то сохраняем по отдельности
        print request.POST
        print "---between--"
        print request.FILES
        for image in images:
            print image
            _album_id=request.POST['album']            
            try:
                _foto = Foto(album_id=_album_id, image=image, title=str(image) )
                _foto.save()
            except Exception, e:
                #messages.error(request, smart_str(e))
                print request
                print smart_str(e)
        
        return redirect('/admin/app/')

admin.site.register(Foto, FotoAdmin)

# video gallery
admin.site.register(Video)

class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title']
    fields = ['title', 'order_num']
admin.site.register(Album, AlbumAdmin)
#admin.site.register(Foto)

#admin.site.register(Place_departure_choices)
#admin.site.register(Subgroup_choices)

### пока не используется 2016.04.07
##admin.site.register(Place_arrival_choices)
##admin.site.register(Tours)