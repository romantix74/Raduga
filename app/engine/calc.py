# -*- coding: utf-8 -*-
from django.conf import settings

from app.models import Director, Participation

####receiver(post_save, sender=Participation )   # посылаем сигнал , после сохранения модели Participation
def Calc(instance, **kwargs):  
    print "====calculation within participations started===="  
    #======ДЕТИ========
    fee_member_kids = 500
    fee_member_kids_discount = 400
    fee_duet_kids = 1400
    fee_duet_kids_discount = 1200
    fee_solo_kids = 800
    fee_solo_kids_discount = 700
    #======ВЗРОСЛЫЕ====
    # плата за одного участника
    fee_member = 500
    # плата за одного участника для доп композиции
    fee_member_discount = 400
    fee_duet = 1500
    fee_duet_discount = 1200
    fee_solo = 800
    fee_solo_discount = 700
    #======спец номинация====
    fee_ensamble_spec = 2000  # плата за всех сразу , по отдельности НЕ берется
    fee_solo_spec = 1000
    fee_other_spec = 1500  # другие форму : дуэты и трио
    
    # общая сумма для руководителя 
    sum_dir = 0
    kid_applications    = Participation.objects.filter(user = instance.user, category = 'kids' )
    kid_0_7             = kid_applications.filter( age_group='0-7')
    kid_8_10            = kid_applications.filter(age_group='8-10')
    kid_hybrid          = kid_applications.filter(age_group='hybrid')

    #kid_applications_duet    = Participation.objects.filter(user = instance.user, category = 'kids' , form_of_execution='duet')

    #kid_applications_solo    = Participation.objects.filter(user = instance.user, category = 'kids' , form_of_execution='solo')

    adult_applications  = Participation.objects.filter(user = instance.user, category = 'adults')
    adult_11_14 = adult_applications.filter( age_group='11-14')
    adult_15_18 = adult_applications.filter( age_group='15-18')
    adult_18_25 = adult_applications.filter( age_group='18-25')
    adult_profi = adult_applications.filter( age_group='profi')
    adult_hybrid = adult_applications.filter( age_group='hybrid')

    #adult_applications_duet = adult_applications.filter(form_of_execution='duet')

    spec_applications   = Participation.objects.filter(user = instance.user, category = 'spec')
    print "CALCCCCCC22"

    # РАСЧЕТ ДЛЯ ВЗРОСЛЫХ
    def _adults(_qset):
        for i,app in enumerate(_qset):
            #находим всех участников из заявки
            count_member = app.list_member   #len(Member.objects.filter(participation__id = app.id))
            print "Count {0}".format(count_member)
            print "I-- {0}".format(i)
            print "app id {0}".format(app.id)
            #global fee_member_kids
            if i == 0:
                print "first app"
                print fee_member_kids
                app.payment = fee_member * count_member
            else:
                print "ELSE app========"
                print fee_member_kids_discount
                app.payment = fee_member_discount * count_member
            print app.payment
                #app.payment = fee_member_kids * count_member
            app.save()
    def _adults_duet(_qset):
        for i,app in enumerate(_qset):
            #находим всех участников из заявки
            count_member = app.list_member            
            if i == 0:                
                app.payment = fee_duet 
            else:                
                app.payment = fee_duet_discount 
            print app.payment
                #app.payment = fee_member_kids * count_member
            app.save()
    def _adults_solo(_qset):
        for i,app in enumerate(_qset):
            #находим всех участников из заявки
            count_member = app.list_member             
            if i == 0:               
                app.payment = fee_solo #* count_member
            else:                
                app.payment = 700 #* count_member  # fee_solo_discount выдает 400 рублей - ПРОВЕРИТЬ 2016.04.21
            print app.payment                
            app.save()
 
    _adults(adult_11_14.filter(form_of_execution='ensamble'))
    _adults(adult_15_18.filter(form_of_execution='ensamble'))
    _adults(adult_18_25.filter(form_of_execution='ensamble'))
    _adults(adult_profi.filter(form_of_execution='ensamble'))
    _adults(adult_hybrid.filter(form_of_execution='ensamble'))

    _adults_duet(adult_11_14.filter(form_of_execution='duet'))
    _adults_duet(adult_15_18.filter(form_of_execution='duet'))
    _adults_duet(adult_18_25.filter(form_of_execution='duet'))
    _adults_duet(adult_profi.filter(form_of_execution='duet'))
    _adults_duet(adult_hybrid.filter(form_of_execution='duet'))

    _adults_solo(adult_11_14.filter(form_of_execution='solo'))
    _adults_solo(adult_15_18.filter(form_of_execution='solo'))
    _adults_solo(adult_18_25.filter(form_of_execution='solo'))
    _adults_solo(adult_profi.filter(form_of_execution='solo'))
    
    print "--------kids--------"
    # РАСЧЕТ ДЛЯ ДЕТЕЙ========================================================================
    def _kids(_qset):
        for i,app in enumerate(_qset):
            #находим всех участников из заявки
            count_member = app.list_member 
            print "app id {0}".format(app.id)
            if i == 0:                
                app.payment = fee_member_kids * count_member
            else:                
                app.payment = fee_member_kids_discount * count_member
            print app.payment
            app.save()
    def _kids_duet(_qset):
        for i,app in enumerate(_qset):
            #находим всех участников из заявки
            count_member = app.list_member 
            if i == 0:                
                app.payment = fee_duet_kids #* count_member
            else:                
                app.payment = fee_duet_kids_discount #* count_member
            print app.payment
            app.save()
    def _kids_solo(_qset):
        for i,app in enumerate(_qset):
            #находим всех участников из заявки
            count_member = app.list_member 
            if i == 0:                
                app.payment = fee_solo_kids #* count_member
            else:                
                app.payment = fee_solo_kids_discount #* count_member
            print app.payment
            app.save()
        
    _kids(kid_0_7.filter(form_of_execution='ensamble'))
    _kids(kid_8_10.filter(form_of_execution='ensamble'))
    _kids(kid_hybrid.filter(form_of_execution='ensamble')) 

    _kids_duet(kid_0_7.filter(form_of_execution='duet'))
    _kids_duet(kid_8_10.filter(form_of_execution='duet'))
    _kids_duet(kid_hybrid.filter(form_of_execution='duet')) 

    _kids_solo(kid_0_7.filter(form_of_execution='solo'))
    _kids_solo(kid_8_10.filter(form_of_execution='solo'))
    _kids_solo(kid_hybrid.filter(form_of_execution='solo'))
    
    # РАСЧЕТ ДЛЯ специальная категория
    for app in spec_applications.filter(form_of_execution = 'solo'):
        app.payment = fee_solo_spec       
        app.save()
    for app in spec_applications.filter(form_of_execution = 'duet'):     
        app.payment = fee_other_spec         
        app.save()
    for app in spec_applications.filter(form_of_execution = 'ensamble'):               
        app.payment = fee_ensamble_spec #* count_member        
        app.save()  

    dir = Director.objects.get(user_id = instance.user)
    dir.payment = sum_dir
    dir.save()