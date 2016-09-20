# -*- coding: utf-8 -*-
from django.conf import settings
import re
import os
from os import path

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import shutil

# исп-ся внтури генерации дипломов
simbols_for_remove = u'\/:*?"<>|»«'   # здесь пробел ПОКА не убирается
def remove(value):  # убираем кавычки и другие запр символы из названия коллектива
    for c in simbols_for_remove:
        value = value.replace(c,'')
    value = re.sub('^\s+|>|<|\n|\r|\s+$', '', value) # удаляем пробелы из конца строки , из начала и символы переноса
    return value
# функция создания дипломов
def generate_diplom( parton , _count):
    print "-----------begin-------"
    print u'{0}'.format( parton.pk)
    _nomination = parton.nomination_output()
    _age_group = parton.age_group_output()    
    
    _collectiv = parton.user if parton.user else parton.user.username  # если не заполнено Название коллектива,то выводим логин  
        
    _collectiv_clear = remove(u'{0}'.format(parton.user))   #parton.user
    
    print u'{0}'.format(_collectiv_clear) 
    print "------------"    
    _institution = parton.user.institution    
    _city = parton.user.city    
    _form_of_execution = parton.form_of_execution  
    _composition_1 = parton.composition_1      
    
    from PIL import Image, ImageDraw, ImageFont
    
    #img = Image.open(path.join(PROJECT_ROOT, 'Raduga02') + "\\" + 'dip_new.jpg') 
    img = Image.open(path.join(settings.PROJECT_ROOT,'dip_clear.jpg'))  # 'dip_new.jpg'
    # E:\RO\!_raduga\diploms\dip_new.jpg)
    
    str_diff = 0 # промежуток между строками
    if (_form_of_execution in ['solo', 'duet']):
        str_diff = 82 
    else:
        str_diff = 120
    
    # get a font
    fnt = ImageFont.truetype(path.join(settings.PROJECT_ROOT,'BKANT.TTF'), 60)
    text_stroka_1 = u"{0} {1}".format(_nomination, _age_group)   #+ "Hello, PIL!!!2222222222222222222222222222222222222222222222"
    color = (255, 0, 120)
    width = img.size[0] 			#Определяем ширину.
    height = img.size[1] 			#Определяем высоту.
    #img = Image.new('RGB', (985, 918), color)
    
    #начало первой строки, для других строк просто добавляем промежуток str_diff
    stroka = height/2+131   # 140
    # первая строка
    imgDrawer = ImageDraw.Draw(img)
    text_width =  imgDrawer.textsize(text_stroka_1, font=fnt)[0]
    text_height =  imgDrawer.textsize(text_stroka_1, font=fnt)[1]
    imgDrawer.text((width/2-text_width/2, stroka), text_stroka_1, font=fnt, fill=(0,0,0, 255))
    
    # вторая строка
    text_stroka_2 = u"{0}".format(_collectiv)
    text_width_2 =  imgDrawer.textsize(text_stroka_2, font=fnt)[0]
    text_height_2 =  imgDrawer.textsize(text_stroka_2, font=fnt)[1]
    stroka += str_diff
    imgDrawer.text((width/2-text_width_2/2, stroka), text_stroka_2, font=fnt, fill=(0,0,0, 255))
    
    # для соло и малой формы
    if (_form_of_execution in ['solo', 'duet']):         
        text_stroka_X = u"{0} {1} {2}".format((parton.member1) if (parton.member1 and _form_of_execution=='duet') else '', 
            u',' + (parton.member2) if (parton.member2 and _form_of_execution=='duet') else '', 
            u','+(parton.member3) if (parton.member3 and _form_of_execution=='duet') else '')
        text_width_X =  imgDrawer.textsize(text_stroka_X, font=fnt)[0]
        text_height_X =  imgDrawer.textsize(text_stroka_X, font=fnt)[1]
        stroka += str_diff
        imgDrawer.text((width/2-text_width_X/2, stroka), text_stroka_X, font=fnt, fill=(0,0,0, 255))
    
    # третья строка
    text_stroka_3 = u"Композиция: \"{0}\" ".format(_composition_1)
    text_width_3 =  imgDrawer.textsize(text_stroka_3, font=fnt)[0]
    text_height_3 =  imgDrawer.textsize(text_stroka_3, font=fnt)[1]
    stroka += str_diff
    imgDrawer.text((width/2-text_width_3/2, stroka), text_stroka_3, font=fnt, fill=(0,0,0, 255))
    
    # четвертая строка
    text_stroka_4 = u"{}{} {}".format(_institution, (',' if _institution and _city else '') ,_city)
    text_width_4 =  imgDrawer.textsize(text_stroka_4, font=fnt)[0]
    text_height_4 =  imgDrawer.textsize(text_stroka_4, font=fnt)[1]
    stroka += str_diff
    imgDrawer.text((width/2-text_width_4/2, stroka), text_stroka_4, font=fnt, fill=(0,0,0, 255))
    
    diplom_dir = path.join(settings.PROJECT_ROOT,'uploads', 'diplom' , u'{0}'.format(_collectiv_clear))
    diplom_dir = diplom_dir.encode('utf-8')
    #print type(diplom_dir)
    #os.chdir(u'/home/ro/Raduga02'+ '/uploads' + '/diplom' + '/'+ u'{0}'.format(_collectiv_clear) )
    #diplom_dir = u'{0}'.format(_collectiv_clear)
    #diplom_dir = remove(diplom_dir)
    print "---before diplom print---"
    print diplom_dir    
    
    if not os.path.exists(diplom_dir):
        os.mkdir(diplom_dir)
    
    #img.save(str(_count) +".png" )
    file_path = path.join(diplom_dir , u'{0}.{1}'.format(remove(_composition_1), "png") ).encode('utf-8')    #_count, "png") ).encode('utf-8')
    print file_path
    img.save(file_path)

# копирование музыки для ранддомного графика
def _cp_music(_qset = None):
    
    folder_uploads = path.join(settings.PROJECT_ROOT,'uploads')
    folder_all_music = path.join(folder_uploads, 'music')
    #for k,v in _qset.iteritems():
        #print k
        #folder_nomination = path.join(folder_uploads, 'music', str(k)) # папки по номинациям
        #if not os.path.exists(folder_nomination):
        #    os.mkdir(folder_nomination)
        #    print u'Создали папку {0}'.format(path.join(folder_uploads, str(k)))
        #if not '_list' in k:  # проверка, что это лист не для итерации листов в шаблоне
        #    print '---list not in k---'
        #    for list in v:
    for i,parton in enumerate(_qset):
        _collectiv = remove(u'{0}'.format(parton.user))    
        print u'{0}'.format(_collectiv)   
                    
        _nomination = remove(parton.nomination_output() )             
        folder_nomination = path.join(folder_uploads, 'music', parton.age_group + '_' +_nomination)
        if not os.path.exists(folder_nomination):
            os.mkdir(folder_nomination)

        _form_of_execution = parton.form_of_execution  
        _composition_1 = remove(parton.composition_1)
                
        print "---"
        print parton.file_music.name
        if parton.file_music.name not in [None, '']:
            _file_music = str(parton.file_music).split('/')[1]
                    
            print "---src_file--"
            src_file = os.path.join(folder_all_music,_file_music)
            print src_file
                    
            print "---dst_file--"
            dst_file = path.join(folder_nomination, _collectiv + '--' + 
                                    _composition_1 +'--' + _file_music[0:8]+ _file_music[-4:])                
            print dst_file
            if path.exists(folder_nomination) and path.exists(src_file):                       
                shutil.copy(src_file , dst_file)
            else:
                print "src_file not_exist"
    print "----"  