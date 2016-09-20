# -*- coding: utf-8 -*-
"""
Definition of models.
"""

from django.db import models
from django.contrib import auth
from django.core.exceptions import ValidationError

from sorl.thumbnail import ImageField
from PIL import Image, ImageDraw

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string

#signals
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# Create your models here.

# News model
def foto_crop(_foto):
    try:
        image = Image.open(_foto)                       
    except IOError:
        print "don't treat"
        #continue
    #image = image.resize((541, 538))
    width = image.size[0] 			#Определяем ширину.
    height = image.size[1] 			#Определяем высоту.

    if height >= width:
        sum = Image.new( 'RGB', (width, width) , (255,255,255)) # create a new white image 
        print u"height is higher"
        diff = height - width     
        for i in xrange(width):
            for j in xrange(width):
                pixel = image.getpixel((i,j+(diff/2)))
                sum.putpixel((i,j),pixel)
        sum.save(_foto)   # перезаписываем первоначальный файл 
    else:  # height < width:
        sum = Image.new( 'RGB', (height, height) , (255,255,255)) # create a new white image 
        print u"width is higher"
        diff = width - height
        for i in xrange(height):
            for j in xrange(height):
                pixel = image.getpixel((i+(diff/2),j))
                sum.putpixel((i,j),pixel)
        sum.save(_foto)
class News(models.Model):    
    class Meta:    # отображение в админке
        verbose_name = u'новость'
        verbose_name_plural = u'новости'

    news_title = models.CharField(max_length = 128)
    news = models.TextField()    
    foto = models.ImageField()
    date_creation = models.DateTimeField(auto_now_add=True,verbose_name=u'Дата создания заявки',
                                         blank = True, null = True)
    #def __str__(self):              # __unicode__ on Python 2
    #    return self.news_title
    def __unicode__(self):
        return u'{}'.format(self.news_title)
    def save(self, *args, **kwargs):
        #do_something()
        print "-----saving NEWS-----------"        
        super(News, self).save(*args, **kwargs) 
        # делаем фотку квадратной , обрезая края
        foto_crop(self.foto.path)
        #отправляем админам письмо о создании новости 
        #_mails = User.objects.filter(is_superuser = 1).values_list('email', flat=True)
        _mails = Director.objects.all().values_list('email', flat=True)        
        # новости - рассылка
        context = {'news' : self}           #'news_title': news.news_title, 'news.foto.url', 'message': message}
        html = render_to_string('app/news_for_mail.html', context)
        #mails =  User.objects.filter(is_superuser = 1).values_list('email', flat=True)
        #if not (self): 
        for mail in _mails:
            try:
                if mail not in ['', None]: #"romantix74" in mail: 
                    print mail
                    send_mail('Новости. "Радуга-танца" г.Чебоксары' , u'{0}'.format(self.news),
                              'dance@radugafest.com', [mail], fail_silently=False,
                              html_message=html)
            except Exception as ex:
                print ex.message

#reglament model
class Reglaments(models.Model):
    class Meta:
        verbose_name = u'положение'
        verbose_name_plural = u'положения'
    reg_title = models.CharField(max_length = 30)
    reg  = models.TextField() 
    def __unicode__(self):
        return u'{}'.format(self.reg_title)

## пока не буду использовать, просто сделаю локальные константы
#class Finance(models.Model):
#    class Meta:    # отображение в админке
#        verbose_name = u'оплата'
#        verbose_name_plural = u'платежи'
#    name = models.CharField(max_length=30, verbose_name=u'Назначение платежа')
#    price = models.FloatField(verbose_name = u'Плата', blank = True, null = True)
#    description = models.CharField(max_length=200, verbose_name=u'Описание платежа, где используется и тд')



Age_groups = (
        ( u'0-7',  u'до 7 лет'),
        ( u'8-10', u'8-10 лет'),
        ( u'11-14', u'11-14 лет'),
        ( u'15-18', u'15-18 лет'),
        ( u'18-25', u'18-25 лет'),
        ( u'hybrid', u'смешанная'),
    )
Approval_choices = (
        ( u'moderacia', u'На модерации'), 
        ( u'warn', u'Внесите исправления'),
        ( u'ok', u'Заявка принята'),    
    )
 

class Director(models.Model):
    class Meta:    # отображение в админке
        verbose_name = u'руководитель'
        verbose_name_plural = u'руководители'

    #user = models.ForeignKey('auth.User')
    user                = models.OneToOneField('auth.User', primary_key=True)
    foto                = models.FileField(blank = True, null = True) #upload_to='./uploads/')
    groupName           = models.CharField(max_length=200, verbose_name=u'Коллектив')
    country             = models.CharField(max_length=200, verbose_name=u'Страна')
    city                = models.CharField(max_length=200, verbose_name=u'Город н/п.')
    director            = models.CharField(max_length=200, verbose_name=u'Руководитель')
    teacher             = models.CharField(max_length=200, verbose_name=u'Педагог/хореограф', blank = True, null = True)
    phoneNumber         = models.CharField(max_length=200, verbose_name=u'Телефон')  #,blank = True, null = True)
    email               = models.CharField(max_length=200, verbose_name=u'E-mail')
    institution         = models.CharField(max_length=200, verbose_name=u'Учреждение', blank = True, null = True) 
    addressInstitution  = models.CharField(max_length=200, verbose_name=u'Адрес учреждения', blank = True, null = True)
    postalAddress       = models.CharField(max_length=200, verbose_name=u'Почтовый адрес', blank = True, null = True)
    site                = models.CharField(max_length=200, verbose_name=u'Сайт', blank = True, null = True)

    date_creation       = models.DateTimeField(auto_now_add=True,verbose_name=u'Дата создания заявки', blank = True, null = True)
    date_change_admin   = models.DateTimeField(verbose_name=u'Дата изменения статуса или комментария модератором',
                                             blank = True, null = True)
    date_change_dir     = models.DateTimeField(verbose_name=u'Дата изменения руководителем',
                                             blank = True, null = True) 
    payment             = models.FloatField(verbose_name = u'Плата', blank = True, null = True)

    def __unicode__(self):        
        #return u"{0} - {1}".format(self.user, self.groupName)
        return u"{0}".format(self.groupName)
    #def __str__(self):              # __unicode__ on Python 2
    #    return str(self.user)          #self.director

# общая для всех модель , в которой прописываем поля , кот-ые есть во всех моделях
class CommonModel(models.Model):
    class Meta:
        abstract = True
        managed = True # странный ключ , если тру, то джанго может управлять таблицами (по умолчанию тру вроде 28.03.16)
    user = models.ForeignKey(Director)      #('auth.User') 
    status = models.CharField( verbose_name = u'Статус', max_length = 100, choices = Approval_choices,
                                blank = True, null = True )
    # комментарии менеджера-админа 
    status_comment = models.TextField(verbose_name = u'Комментарий', blank = True, null = True)
    date_creation = models.DateTimeField(auto_now_add=True,verbose_name=u'Дата создания заявки', blank = True, null = True)
    date_change_admin = models.DateTimeField(verbose_name=u'Дата изменения статуса или комментария модератором',
                                             blank = True, null = True)
    date_change_dir   = models.DateTimeField(verbose_name=u'Дата изменения руководителем',
                                             blank = True, null = True)  
class Common_with_finance_Model(CommonModel):
    class Meta:
        abstract = True
    payment = models.FloatField(verbose_name = u'Плата', blank = True, null = True)

Gender_choices = (
    (u'male', u'М'),
    (u'female', u'Ж')
    )

# Member model , 
def make_upload_path(instance, filename):
    """Generates upload path for FileField"""
    return u"scan/%s-%s" % (instance.user.groupName, instance.user.id) # filename)
class Member(CommonModel):     #(models.Model):  
    class Meta:    # отображение в админке
        verbose_name = u'участник'
        verbose_name_plural = u'участники'
          
    age_group = models.CharField(verbose_name=u'Возрастная группа', max_length=10, choices=Age_groups)    
    #для отображения в темплейте значений, а не ключей словаря
    def age_group_output(self):
        return u'{}'.format(self.get_age_group_display())
    
    first_name = models.CharField(verbose_name = u'Имя', max_length=30)
    last_name = models.CharField(verbose_name = u'Фамилия', max_length=30)
    middle_name = models.CharField(verbose_name = u'Отчество' ,max_length=30, blank=True)
    age = models.IntegerField(verbose_name = u'Возраст')     
    gender = models.CharField(verbose_name = u'Пол', max_length = 10, choices = Gender_choices) 
    def gender_output(self):
        return u'{}'.format(self.get_gender_display())

    scan_passport = ImageField(verbose_name = u'Скан документа, удостоверяющего личность', 
                                upload_to=make_upload_path,    
                                blank=True, null = True)    
    #scan_passport.short_description = u'Скан'

    # админка
    def display_groupName(self):    
        return Director.objects.get(user = self.user).groupName  
    display_groupName.short_description = u'Коллектив участника'

    def __unicode__(self):        
        return u"{0} {1} {2} - {3} лет".format(self.first_name, self.last_name, self.middle_name, self.age)

    #проверяем загружена ли фотка , Если нет, то выводим ошибку
    def clean_fields(self, exclude=None):        
        if not (self.scan_passport ):            
            raise ValidationError(u'Загрузите фото')        

#используется в Participation
class Subgroup_choices(models.Model):
    user = models.ForeignKey('auth.User')
    subgroup_name = models.CharField( max_length = 100)        
    def __unicode__(self):    
        return self.subgroup_name

# Participation model  
def make_upload_path_music(instance, filename):
    """Generates upload path for FileField"""
    print filename.split('.')[-1]
    print "afetr extension-------"
    return u"music/{0}__{1}.{2}".format(instance.user.pk, instance.id, filename.split('.')[-1]) # расширение берем сплитом
class Participation(Common_with_finance_Model):    
    
    class Meta:    # отображение в админке
        verbose_name = u'заявка на участие'
        verbose_name_plural = u'заявки на участие'
    
    category_choices = (        
        (u'adults', u'Радуга-танца'),
        (u'kids',   u'Радуга-танца KIDS'),
        (u'spec',   u'Спец. номинация'),
        #('adults' , 'adult'),
        #('kids' , 'kids'),
    )
    category = models.CharField(verbose_name=u'Категория', max_length = 30 , choices = category_choices ) 
    #для отображения в темплейте значении, а не ключей словаря
    def category_output(self):
        return self.get_category_display()
    nomination_choices = (
        #('estrada' , 'estrada'),
        #('narod' , 'narod'),
        #('narod_style' , 'narod_style'),
        #('sovremen_svobod' , 'sovremen_svobod'),  
        
        ('estrada' , u'Эстрадный танец'),
        ('narod' , u'Народный танец'),
        ('narod_style' , u'Народный стилизованный танец'),
        ('sovremen_svobod' , u'Современный танец (свободная пластика)'),
        ('sovremen_ulica' , u'Современный танец (уличный танец)'),
        #('classic' , u'Классический танец'),
        ('narod+_narod_style' , u'Народный танец, народный стилизованный танец'),
        ('suget-igrovoi' , u'Сюжетно-игровой танец'), 
        ('spec' , u'Великой победе посвящается'),            
    )
    nomination = models.CharField(verbose_name=u'Номинация', max_length = 30 , choices = nomination_choices )
    def nomination_output(self):
        return self.get_nomination_display()
    age_group = models.CharField(verbose_name=u'Возрастная группа', max_length=10 , choices = Age_groups )
    def age_group_output(self):
        return self.get_age_group_display()     
    subgroup = models.ForeignKey(Subgroup_choices, \
                                verbose_name=u'Подгруппа коллектива', max_length = 30, blank = True, null = True ) 
    #def subgroup_output(self):
    #    return self.get_subgroup_display()
    form_of_execution_choices = (
        (u'solo', u'соло'),
        (u'duet', u'малая форма'),
        (u'ensamble', u'ансамбль'),        
    )
    form_of_execution = models.CharField(verbose_name=u'Форма исполнения', max_length = 10 , choices = form_of_execution_choices ) 
    def form_of_execution_output(self):
        return self.get_form_of_execution_display()
    list_member = models.IntegerField(verbose_name=u'Количество участников')
    member1         = models.CharField(verbose_name=u'Участник N1', max_length = 50 , blank = True, null = True)
    member2         = models.CharField(verbose_name=u'Участник N2', max_length = 50 , blank = True, null = True)
    member3         = models.CharField(verbose_name=u'Участник N3', max_length = 50 , blank = True, null = True)
    #list_member     = models.ManyToManyField(Member,verbose_name=u'Список участников')
    composition_1   = models.CharField(verbose_name=u'Композиция', max_length = 200 )
    description_comp = models.TextField(verbose_name=u'Описание к танцу', max_length = 2000, blank = True, null = True )
    # не используются
    count_member_1  = models.IntegerField(verbose_name=u'Количество участников', blank = True, null = True)     
    composition_2   = models.CharField(verbose_name=u'Композиция №2', max_length = 200, blank = True, null = True)
    count_member_2  = models.IntegerField(verbose_name=u'Количество участников', blank = True, null = True)
    file_music      = models.FileField(verbose_name=u'Аудиозапись',
                                      upload_to = make_upload_path_music,    #"./music/",
                                      blank = True, null = True)
    place           = models.CharField(verbose_name=u'Место', max_length = 30, blank = True, null = True)

    # для админки, отображения Коллектива, за место имени руководителя
    def collective_show(self):    
        return Director.objects.get(user_id = self.user_id).groupName    
    collective_show.short_description = u'Коллектив'
    def city_show(self):    
        return Director.objects.get(user_id = self.user_id).city    
    city_show.short_description = u'Город'

    ## для админки, отображения Списка участников
    #def list_member_show(self):    
    #    return ', '.join([ str(i) for i in self.list_member.all() ])    
    #list_member_show.short_description = u'Список участников'
    
    ## для админки, отображения общего количества Списка участников
    #def list_member_count(self):    
    #    return self.list_member.all().count()   
    #list_member_count.short_description = u'Кол-во уч-ков'
    
    #def list_member_male_count(self):    
    #    return self.list_member.filter(gender = 'male').count()   
    #list_member_male_count.short_description = u'Кол-во уч-ков М'
    
    #def list_member_female_count(self):    
    #    return self.list_member.filter(gender = 'female').count()   
    #list_member_female_count.short_description = u'Кол-во уч-ков Ж'

    #def __str__(self):              # __unicode__ on Python 2
    def __unicode__(self):
        #return str(self.user)
        return u"{0}".format(self.user)
    #def save(self, *args, **kwargs):
        #do_something()
        #print '---calc in models------'
       
        #Calc(self)        
        #super(Participation, self).save(*args, **kwargs) 
    #проверяем загружена ли аудиозапись , Если нет, то выводим ошибку
    #def clean_fields(self, exclude=None):        
    #    if not (self.file_music ):            
    #        raise ValidationError(u'Загрузите аудиозапись')


# Residing - проживание
class Residing(Common_with_finance_Model):    
    
    class Meta:    # отображение в админке
        verbose_name = u'проживание'
        verbose_name_plural = u'заявки на проживание'

    place_of_residing_choices = (        
        ('dush4', u'СДЮСШОР №4'),
        ('dush3', u'СДЮСШОР №3'),
        ('admiral', u'Гостиница «Адмирал»'),
        ('salampi', u'Cанаторий «Салампи»'),
        ('nadegda', u'Санаторий "Надежда"'),
        ('nikolaeva', u'Гостиница АУ "Центральный Стадион им. А.Г. Николаева"'),
        ('Chgpu' , u'Санаторий профилакторий ЧГПУ им. И.Я. Яковлева "Мечта"'),
        ('Gemchugina' , u'Оздоровительный комплекс "Жемчужина Чувашии"'),
    )
    place_of_residing = models.CharField(verbose_name=u'Место проживания', max_length = 30, choices = place_of_residing_choices )   
    def place_of_residing_output(self):
        return self.get_place_of_residing_display()
    quantity_total    = models.IntegerField(verbose_name=u'Общее количество проживающих')
    quantity_adult_male    = models.IntegerField(verbose_name=u'Количество взрослых М')
    quantity_adult_female  = models.IntegerField(verbose_name=u'Количество взрослых Ж')
    quantity_member_male   = models.IntegerField(verbose_name=u'Количество участников М')
    quantity_member_female = models.IntegerField(verbose_name=u'Количество участников Ж')
    date_arrival      = models.DateField(verbose_name=u'Дата заезда')
    time_arrival      = models.TimeField(verbose_name=u'Время заезда')
    date_departure    = models.DateField(verbose_name=u'Дата отъезда')
    time_departure    = models.TimeField(verbose_name=u'Время отъезда')   

    # для админки, отображения Коллектива, за место имени руководителя
    def mail_show(self):    
        return Director.objects.get(user_id = self.user_id).email
    mail_show.short_description = u'E-mail'
    def __unicode__(self):
        #return str(self.user)
        return u"{0}".format(self.user)

# используеться в Трансфера и Экскурсиях для мест отбытия и прибытия одновременно
class Place_departure_choices(models.Model):
    user = models.ForeignKey('auth.User')
    place_name = models.CharField( max_length = 100)
    description = models.TextField(blank = True, null = True)
    #def __str__(self):              # __unicode__ on Python 2
    def __unicode__(self):    
        return self.place_name
class Place_arrival_choices(models.Model):
    place_name = models.CharField( max_length = 100)
    description = models.TextField()
    #def __str__(self):              # __unicode__ on Python 2
    def __unicode__(self):    
        return self.place_name


#### Transfer
class Transfer(Common_with_finance_Model):     
    
    class Meta:    # отображение в админке
        verbose_name = u'трансфер'
        verbose_name_plural = u'заявки на трансфер'
    
    date_departure = models.DateField(verbose_name=u'Дата отбытия')
    time_departure = models.TimeField(verbose_name=u'Время отбытия')    
    place_departure = models.ForeignKey(Place_departure_choices, 
                                        verbose_name=u'Место отбытия', max_length = 30,
                                        related_name = 'place_departure', 
                                        null = True,  blank = True )    
    place_arrival   = models.ForeignKey(Place_departure_choices, 
                                        verbose_name=u'Место прибытия', max_length = 30, 
                                        related_name = 'place_arrival',
                                        null = True,  blank = True )
    def place_arrival_output(self):
        return self.get_place_arrival_display()
    quantity_total  = models.IntegerField(verbose_name=u'Количество общее')   
    quantity_adult  = models.IntegerField(verbose_name=u'Количество взрослых')
    quantity_member = models.IntegerField(verbose_name=u'Количество участников')

    def __unicode__(self):
        #return str(self.user)
        return u"{0}".format(self.user)

# Excursion
# База для добавления экскурсий , ПОКА не используется
class Tours(models.Model):
    tour_name = models.CharField( max_length = 30)
    description = models.TextField()
    #def __str__(self):              # __unicode__ on Python 2
    def __unicode__(self):    
        #return str(self.tour_name)
        return u"{0}".format(self.tour_name)

class Excursion(Common_with_finance_Model):    
    
    class Meta:    # отображение в админке
        verbose_name = u'экскурсия'
        verbose_name_plural = u'заявки на экскурсии'
    
    #tour_choice = models.ForeignKey(Tours,verbose_name=u'Форма экскурсии')  
    tour_form_choices = (
        ('EveningCheb' , u'Вечерние Чебоксары'),
        ('obzorCheb' , u'Обзорная экскурсия по г. Чебоксары'),
    )
    tour_form = models.CharField(verbose_name=u'Форма экскурсии', max_length = 100, choices = tour_form_choices)  
    def tour_form_output(self):
        return self.get_tour_form_display()
    date_departure = models.DateField(verbose_name=u'Дата отбытия')
    time_departure = models.TimeField(verbose_name=u'Время отбытия')
    #place_departure = models.CharField(verbose_name=u'Место отбытия', max_length = 30)
    place_departure = models.ForeignKey(Place_departure_choices , verbose_name=u'Место отбытия',
                                        related_name = 'ex_place_departure',
                                        max_length = 30, null = True, blank = True )
    #place_arrival = models.CharField(verbose_name=u'Место прибытия', max_length = 30)
    place_arrival = models.ForeignKey(Place_departure_choices, verbose_name=u'Место прибытия', 
                                      related_name = 'ex_place_arrival',
                                      max_length = 30, null = True,  blank = True )
    quantity_total = models.IntegerField(verbose_name=u'Количество общее')   
    quantity_adult = models.IntegerField(verbose_name=u'Количество взрослых')
    quantity_member = models.IntegerField(verbose_name=u'Количество участников')
      
    def __unicode__(self):
        #return str(self.user)    #.username + ' ' +self.tour_choice)
        return u"{0}".format(self.tour_form)
