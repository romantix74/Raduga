# -*- coding: utf-8 -*-
"""
Definition of forms.
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django.utils.translation import ugettext_lazy as _

from models import CommonModel,Member, Participation, Director, Residing, Transfer, \
                    Excursion, Subgroup_choices, Place_departure_choices, Food, Mails
from django.forms.extras.widgets import SelectDateWidget
#from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget
from django.forms import widgets
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset, MultiField 
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
#from bootstrap3_datetime.widgets import DateTimePicker
#from app.fields import PartonSubgroupField
from django.contrib import auth
from django.http import HttpRequest

from captcha.fields import CaptchaField
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)

from django.utils.text import capfirst

#форма обратной связи
class FeedbackForm(forms.Form):
    user_mail = forms.EmailField(label=u'Ваш email',
                            widget=forms.EmailInput(attrs={'class': 'email', 'placeholder': 'Email','name':'email'}),
                            error_messages={'required': u'Введите свой email адрес'})
    user_question = forms.CharField(max_length=1000,
        label =  u'Ваш вопрос',
        widget = forms.Textarea(attrs={'class': 'contact_user_question',
                                       'placeholder': u'Опишите вашу проблему или оставьте комментарий',
                                       'name':'user_question'}),
        error_messages={'required': u'Задайте вопрос'})
    captcha = CaptchaField()
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'form-horizontal'        
        self.helper.label_class = 'col-xs-2'
        self.helper.field_class = 'col-xs-8'        
        self.helper.layout.append(
            FormActions(
                HTML( u"""<div class="modal-footer">
                            <input type="submit" name="save" value="Отправить" class="btn btn-primary">
                            <a role="button" class="btn btn-default" data-dismiss="modal">Отмена</a>
                     </div>"""),         
        ))

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': u'Логин'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': u'Пароль'}))
    #error_messages = {
    #    'invalid_login': _(u"Пожалуйста, введите корректное имя пользователя и пароль. "),
    #                       #Note that both fields may be case-sensitive."),
    #    'inactive': _(u"Аккаунт не активен, обратитесь к администрации."),
    #}

class UserRegistrationForm(forms.ModelForm):   #UserCreationForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    #username = models.CharField(
    #    _('username'),
    #    max_length=30,
    #    unique=True,
    #    help_text= _('Обязательное поле.'),    #_('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    #    validators=[
    #        #validators.RegexValidator(
    #        #    r'^[\w.@+-]+$',
    #        #    _('Enter a valid username. This value may contain only '
    #        #      'letters, numbers ' 'and @/./+/-/_ characters.')
    #        #),
    #    ],
    #    error_messages={
    #        'unique': _("A user with that username already exists."),
    #    },
    #)
    email = forms.CharField(label=_("E-mail"),
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'E-mail'}))
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as before, for verification."))
    #captcha = CaptchaField()    # widget=forms.TextInput(attrs={'class': 'form-control'}))
    ##widgets = { 'captcha' : forms.TextInput( attrs = {'class': 'form-control'}) }
    class Meta:
        model = User
        fields = ("username",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        user = super(forms.ModelForm, self).save(commit=False)         #UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]          
        if commit:
            user.save()            
        return user

    
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-RegistrationForm'
        self.helper.form_class = 'form-horizontal'        
        self.helper.label_class = 'col-xs-3'
        self.helper.field_class = 'col-xs-8'
        #self.helper.layout(
        #    StrictButton('Sign in', css_class='btn-default'),    
        #)
        self.helper.layout.append(
            FormActions(
                HTML( u"""<div class="modal-footer">
                            <input type="submit" name="save" value="Зарегистрироваться" class="btn btn-primary">
                            <a role="button" class="btn btn-default" data-dismiss="modal">Отмена</a>
                     </div>"""),                      
                #Submit('save', 'Submit'),
        ))
    
class MemberForm(forms.ModelForm):    
    class Meta:
        model = Member
        fields = ['age_group', 'first_name', 'last_name', 'age', 'gender', 'scan_passport']                   
        widgets = {
            'age_group' :    forms.Select(attrs = {'class': 'input-sm' , 'id' : 'member_age_group'},),
            'first_name' :   forms.TextInput( attrs = {'class': 'input-sm', 'id' : 'member_first_name'},                                            ),
            'last_name' :    forms.TextInput( attrs = {'class': 'input-sm', 'id' : 'member_last_name'}), 
            #'middle_name' : forms.TextInput( attrs={'class': 'input-sm' , 'id': 'member_middle_name'} ),
            'age'          : forms.NumberInput( attrs = {'class': 'input-sm' , 'id': 'member_age'} ),   
            'gender'       : forms.Select( attrs = {'class': 'input-sm', 'id': 'member_gender' }),
            'scan_passport': forms.FileInput( attrs = {'class': 'input-sm' , 'id': 'member_scan_passport'} ),          
        }
        error_messages = {
            'age_group':  {'required': _(u"Необходимо выбрать возрастную группу!"), },
            'first_name': {'required': _(u"Необходимо ввести имя участника!"), },
            'last_name': {'required': _(u"Необходимо ввести фамилию участника!"), },
            'age':       {'required': _(u"Необходимо ввести возраст участника!"), },
            'gender':       {'required': _(u"Необходимо ввести пол участника!"), },
            'scan_passport': {'required':
                              _(u"Загрузите скан копию документа  участника (свидетельство о рождении, паспорт)!"), },
        }

    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'form-horizontal'        
        self.helper.label_class = 'col-xs-2'
        self.helper.field_class = 'col-xs-8'        
        self.helper.layout.append(
            FormActions(
                HTML( u"""<div class="modal-footer">                            
                            <input type="submit" name="save" value="Готово" class="btn btn-primary">              
                            <a role="button" class="btn btn-default" data-dismiss="modal">Отмена</a>
                     </div>"""),                 
        ))

class ParticipationForm(forms.ModelForm):
      
    class Meta:
        model = Participation        
        #exclude = ['user']
        fields = ['category', 'nomination', 'age_group','subgroup', 'form_of_execution', 
                'list_member', 'member1', 'member2', 'member3', 'composition_1', 'file_music', 'description_comp'] 
                 #'count_member_1', 'composition_2', 'count_member_2']      
        widgets = {
            'category'          : forms.Select( attrs={'class': 'input-sm', 'id' : 'prtcp_category'}),
            'nomination'        : forms.Select( attrs={'class': 'input-sm', 'id' : 'prtcp_nomination'}),
            'age_group'         : forms.Select( attrs={'class': 'input-sm', 'id' : 'prtcp_age_group'}),             
            'subgroup'          : forms.Select( attrs={'class': 'input-sm', 'id' : 'prtcp_subgroup'} ),
            #'subgroup_choice'   : forms.CheckboxInput(attrs={'class': 'input-sm', 'id': 'prtcp_subgroup_choice'}),
            'form_of_execution' : forms.Select( attrs={'class': 'input-sm', 'id': 'prtcp_form_of_execution'} ),            
            'list_member'       : forms.NumberInput( attrs= {'class': 'input-sm', 'id': 'prtcp_list_member'} ),    #forms.SelectMultiple( attrs= { 'id': 'prtcp_list_member'} ), 
            'member1'           : forms.TextInput(attrs={'class': 'input-sm' , 'id': 'prtcp_member1', 
                                                         'placeholder': u'Иванов Иван Иванович',} ),
            'member2'           : forms.TextInput(attrs={'class': 'input-sm' , 'id': 'prtcp_member2', 
                                                         'placeholder': u'Иванов Иван Иванович',} ),
            'member3'           : forms.TextInput(attrs={'class': 'input-sm' , 'id': 'prtcp_member3',
                                                         'placeholder': u'Иванов Иван Иванович',} ),
            'composition_1'     : forms.TextInput(attrs={'class': 'input-sm' , 'id': 'prtcp_composition_1'} ),
            'file_music'        : forms.FileInput(attrs={'class': 'input-sm' , 'id': 'prtcp_file_music'} ),
            'description_comp'  : forms.Textarea( attrs={'class': 'input-sm' , 'id': 'prtcp_description_comp'} ),
            #'count_member_1'    : forms.NumberInput(    attrs={'class': 'input-sm' , 'id': 'prtcp_count_member_1'} ),
            #'composition_2'     : forms.TextInput(      attrs={'class': 'input-sm' , 'id': 'prtcp_composition_2'} ),
            #'count_member_2'    : forms.NumberInput(    attrs={'class': 'input-sm' , 'id': 'prtcp_count_member_2'} ),           
        }   
        help_texts = {
            'category': _(u'Необходимо выбрать только один элемент'),
        } 
        error_messages = {
            'category'      :   {'required': _(u"Необходимо выбрать категорию!"), },
            'nomination'    :   {'required': _(u"Необходимо выбрать  номинацию!"), },
            'age_group'     :   {'required': _(u"Необходимо выбрать возрастную группу!"), },
            'subgroup'      :   {'required': _(u"Необходимо выбрать или ввести название подгруппы!"), },
            'form_of_execution':{'required': _(u"Необходимо выбрать форму исполнения!"), },
            'list_member'   :   {'required': _(u"Необходимо выбрать, как минимум одного участника!"), },
            'composition_1' :   {'required': _(u"Необходимо ввести название композиции!"), },
            'file_music'    :   {'required': _(u"Необходимо приложить аудиозапись!"), },
            #'description_comp':  {'required': _(u"Необходимо ввести название композиции!"), },
                      
        }

    def __init__(self, *args, **kwargs):                       
        
        # фильтрация в subgroup
        _user = kwargs.pop('_user', None)   # в этом параметре берем юзер_ид (директора) для фильтрации в subgroup
        
        super(ParticipationForm, self).__init__(*args, **kwargs)         
        
        # заполняем названия в поле выбора , которые используются самими участниками
        self.fields['subgroup'].choices = [('', '--------')] + [('-1', u'младшая')]  \
                         + [('-2', u'средняя')] + [('-3', u'старшая')] \
                         + list(Subgroup_choices.objects.filter(user_id = _user).values_list('id', 'subgroup_name'))  

        ## 2016.03.24
        #def filterForField_listMember(_list_members):
        #    for i, _mb in enumerate(_list_members):                
        #        new_tuple = tuple([_mb[0], _mb[1] + ' ' + _mb[2]])
        #        _list_members.pop(i)
        #        _list_members.insert(i, new_tuple)                
        ##_list_members_do7 = list(Member.objects.filter(user_id =_user,age__lt = 7).values('id', 'LastName'))
        #_list_members_do7   = list(Member.objects.filter(user_id = _user, age_group = '0-7').values_list('id','last_name','first_name'))
        #filterForField_listMember(_list_members_do7)
        #_list_members_8_10  = list(Member.objects.filter(user_id = _user, age_group = '8-10').values_list('id','last_name','first_name'))
        #filterForField_listMember(_list_members_8_10)
        #_list_members_11_14 = list(Member.objects.filter(user_id = _user, age_group = '11-14').values_list('id','last_name','first_name'))
        #filterForField_listMember(_list_members_11_14)
        #_list_members_15_18 = list(Member.objects.filter(user_id = _user, age_group = '15-18').values_list('id','last_name','first_name'))
        #filterForField_listMember(_list_members_15_18)
        #_list_members_19_25 = list(Member.objects.filter(user_id = _user, age_group = '19-25').values_list('id','last_name','first_name'))
        #filterForField_listMember(_list_members_19_25)       
        
        ## переход на ПРОСТО кол-во участников 2016.03.24
        #self.fields['list_member'].choices = [(u'0-7 лет', _list_members_do7
        #                                              #(
        #                                              #  ('1', 'member1'),
        #                                              #  ('12', 'member12')
        #                                              #)
        #                                       ) , 
        #                                      (u'8-10 лет', _list_members_8_10 ),
        #                                      (u'11-14 лет', _list_members_11_14 ),
        #                                      (u'15-18 лет', _list_members_15_18 ),
        #                                      (u'19-25 лет', _list_members_19_25 ),
        #                                    ]
        
        # для красивой формы
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-ParticipationForm'
        self.helper.form_class = 'form-horizontal'        
        self.helper.label_class = 'col-xs-2'
        self.helper.field_class = 'col-xs-8'        
        self.helper.layout.append(
            FormActions(
                HTML( u"""<div class="modal-footer">
                            <input type="submit" name="save" value="Готово" class="btn btn-primary">
                            <a role="button" class="btn btn-default" data-dismiss="modal">Отмена</a>
                     </div>"""),                      
                #Submit('save', 'Submit'),
    ))    
    
    def clean_list_member(self):
        data = self.cleaned_data['list_member']        
        if data  > 25 :    #.count() > 25 :
            raise forms.ValidationError(u"Количество участников в заявке не должно превышать 25 человек")
        return data
    
    def clean(self):
        cleaned_data = super(ParticipationForm, self).clean()         
        _form_of_execution    = cleaned_data.get('form_of_execution') 
        _list_member  = cleaned_data.get('list_member')         
        ##_count_member = cleaned_data.get('quantity_member') if cleaned_data.get('quantity_member') else 0  
        #_count_member = cleaned_data.get('list_member').count() if cleaned_data.get('list_member') else 0              
        _count_member = _list_member if _list_member else 0
        # если не сделать эту проверку , будет ругаться на nontype        
        #if ( _form_of_execution == 'solo' and _list_member.count() != 1 ):  
        if ( _form_of_execution == 'solo' and _count_member != 1 ):                            
            raise forms.ValidationError(u'В форме исполнения "соло" количество участников должно быть равно одному') 
        if ( _form_of_execution == 'duet' and (_count_member not in [2,3]) ):                                
            raise forms.ValidationError(u'В форме исполнения "Малая форма" количество участников должно быть равно двум или трем') 
        # Делаем поля с ФИО обязательными , для соло - одно поле, для малой формы - 2 поля
        _member1 = cleaned_data.get('member1')
        _member2 = cleaned_data.get('member2')
        
        if ( _form_of_execution == 'solo' and (_member1 is None)):
            raise forms.ValidationError(u'Заполните поле Участник №1') 
        if ( _form_of_execution == 'duet' and (_member1 is None) and (_member2 is None)):
            raise forms.ValidationError(u'Заполните поля Участник №1 и Участник №2')       


class DirectorUploadFile(forms.ModelForm):
    class Meta:
        model = Director
        fields = ['foto']

class DirectorEditForm(forms.ModelForm):
    #class Media:
    #    css = {
    #        'all': ('app/content/jquery.kladr.min.css',)
    #    }
    #    js = ('app/scripts/jquery.kladr.min.js',)
    class Meta:
        model = Director
        #exclude = ['user' , 'foto']
        fields = ['groupName', 'country', 'region', 'city', 'street', 'homeNumber',
                  'director', 'teacher', 'phoneNumber', 'email', 'institution',
                   'site']
                  #'addressInstitution', 'site']
        widgets = {
            'groupName'         : forms.TextInput( attrs={'class': 'input-sm forHover', 'id': 'dir_groupName',
                                                          'placeholder': 'Хореографический коллектив "Радуга"'}),
            'country'           : forms.Select( attrs={'class': 'input-sm forHover', 'id': 'dir_country',
                                                          'placeholder': 'Россия'}),
            'region'            : forms.TextInput( attrs={'class': 'input-sm forHover', 'id': 'dir_region',
                                                          'placeholder': 'Чувашская'}),
            'city'              : forms.TextInput( attrs={'class': 'input-sm forHover', 'id': 'dir_city', 
                                                          'placeholder': 'Новочебоксарск'}),
            'street'            : forms.TextInput( attrs={'class': 'input-sm forHover', 'id': 'dir_street',
                                                          'placeholder': 'Строителей'}),
            'homeNumber'        : forms.TextInput( attrs={'class': 'input-sm forHover', 'id': 'dir_homeNumber',
                                                          'placeholder': '2'}),
            'director'          : forms.TextInput( attrs={'class': 'input-sm forHover', 'id': 'dir_director', 
                                                          'placeholder': 'Иванов Иван Иванович'}),             
            'teacher'           : forms.TextInput( attrs={'class': 'input-sm forHover', 'id': 'dir_teacher',
                                                          'placeholder': 'Петров Петр Петрович'} ),            
            'phoneNumber'       : forms.TextInput( attrs={'class': 'input-sm forHover', 'id': 'dir_phoneNumber',
                                                          'placeholder': '+7-917-123-45-67'} ),            
            'email'             : forms.EmailInput( attrs={'class': 'input-sm forHover', 'id': 'dir_email',
                                                          'placeholder': 'box@mail.ru'} ), 
            'institution'       : forms.TextInput( attrs={'class': 'input-sm forHover', 'id': 'dir_institution',
                                                          'placeholder': 'Дворец Культуры "Химик"'} ),
            #'addressInstitution': forms.TextInput( attrs={'class': 'input-sm forHover', 'id': 'dir_addressInstitution',
            #                                              'placeholder': 'г. Новочебоксарск, Ул. Винокурова 2'} ),
            'postalAddress'     : forms.TextInput( attrs={'class': 'input-sm forHover', 'id': 'dir_postalAddress'} ),
            'site'              : forms.TextInput( attrs={'class': 'input-sm forHover', 'id': 'dir_site',
                                                          'placeholder': 'radugafest.com'} ),           
        }
        #initial = {
        #    'email'             :
        #}
    def __init__(self, *args, **kwargs):
        super(DirectorEditForm, self).__init__(*args, **kwargs)
        setup_bootstrap_helpers(self, 'id-DirectorEditForm')
        #self.helper = FormHelper(self)
        #self.helper.form_id = 'id-DirectorEditForm'
        #self.helper.form_class = 'form-horizontal'        
        #self.helper.label_class = 'col-xs-2'
        #self.helper.field_class = 'col-xs-8 col-xs-offset-1'        
        #self.helper.layout.append(
        #    FormActions(
        #        HTML(u"""<div class="modal-footer">
        #                    <input type="submit" name="save" value="Готово" class="btn btn-primary">
        #                    <a role="button" class="btn btn-default" data-dismiss="modal">Отмена</a>
        #             </div>"""),       
        #))

# прикрепляем классы и футер к модальной форме
def setup_bootstrap_helpers(object, _id):
    object.helper = FormHelper(object)
    object.helper.form_id = '_id'  # возможно не используеться
    object.helper.form_class = 'form-horizontal'        
    object.helper.label_class = 'col-xs-2'
    object.helper.field_class = 'col-xs-8 col-xs-offset-1'        
    object.helper.layout.append(
        FormActions(
            HTML(u"""<div class="modal-footer">
                        <input type="submit" name="save" value="Готово" class="btn btn-primary">
                        <a role="button" class="btn btn-default" data-dismiss="modal">Отмена</a>
                    </div>"""),       
    ))

timeOptions = {
#'format': 'HH:ii:ss',
'format': 'HH:ii',
'autoclose': True,
#'showMeridian' : True
}
dateOptions = {
'format': 'yyyy-mm-dd ',
'autoclose': True,
#'showMeridian' : True
}

dateOptionsPicker = {
    #'autoclose': True, 'format': "yyyy-mm-dd", 'minView': "month"
    "format": "YYYY-MM-DD", "pickTime": False
}
class ResidingForm(forms.ModelForm):
    class Meta:
        model = Residing
        #exclude = ['user']
        #fields = ['place_of_residing' , 'quantity_total' , 'quantity_adult', 'quantity_member' , 'date_arrival' ,'time_arrival','date_departure','time_departure']
        fields = ['place_of_residing' , 'quantity_total', 'quantity_adult_male',
                 'quantity_adult_female', 'quantity_member_male', 'quantity_member_female',
                 'date_arrival' ,'time_arrival','date_departure','time_departure']
        widgets = {
            'place_of_residing' : forms.Select(      attrs={'class': 'input-sm' , 'id': 'rsd_place_of_residing'}),
            'quantity_total'    : forms.NumberInput( attrs={'class': 'input-sm' , 'id': 'rsd_quantity_total'}),
            'quantity_adult_male'   : forms.NumberInput( attrs={'class': 'input-sm', 'id': 'rsd_quantity_adult_male'}),
            'quantity_adult_female' : forms.NumberInput( attrs={'class': 'input-sm', 'id': 'rsd_quantity_adult_female'}),
            'quantity_member_male'  : forms.NumberInput( attrs={'class': 'input-sm', 'id': 'rsd_quantity_member_male'}),
            'quantity_member_female': forms.NumberInput( attrs={'class': 'input-sm', 'id': 'rsd_quantity_member_female'}),
            #'date_arrival'   : DateWidget(options = dateOptions, attrs={'class': 'input-sm', 'id': 'rsd_date_arrival'}, usel10n = True, bootstrap_version=3), 
            'date_arrival'   : forms.TextInput( attrs={'class': 'input-sm', 'id': 'rsd_date_arrival'}), 
            'time_arrival'   : forms.TextInput( attrs={'class': 'input-sm', 'id': 'rsd_time_arrival'}),
            'date_departure' : forms.TextInput( attrs={'class': 'input-sm', 'id': 'rsd_date_departure'}),
            'time_departure' : forms.TextInput( attrs={'class': 'input-sm', 'id': 'rsd_time_departure'}),   
        }
        error_messages = {
            'place_of_residing':        {'required': _(u"Выберите место проживания!"), },
            'quantity_total':           {'required': _(u"Укажите общее количество проживающих!"), },
            'quantity_adult_male':      {'required': _(u"Укажите количество взрослых-мужчин!"), },
            'quantity_adult_female':    {'required': _(u"Укажите количество взрослых-женщин!"), },
            'quantity_member_male':     {'required': _(u"Укажите количество участников-мальчиков!"), },
            'quantity_member_female':   {'required': _(u"Укажите количество участников-девочек!"), },
            'date_arrival':             {'required': _(u"Укажите дату заезда!"), },  
            'time_arrival':             {'required': _(u"Укажите время заезда!"), },
            'date_departure':           {'required': _(u"Укажите дату отъезда!"), },
            'time_departure':           {'required': _(u"Укажите время отъезда!"), },          
        }
    def __init__(self, *args, **kwargs):
        _user = kwargs.pop('_user', None)   # в этом параметре берем юзер_ид (директора) для фильтрации ПОКА не используется ,но сделал по аналогии с экскурсиями и трансферами
        super(ResidingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-ResidingForm'
        self.helper.form_class = 'form-horizontal'        
        self.helper.label_class = 'col-xs-2'
        self.helper.field_class = 'col-xs-8'        
        self.helper.layout.append(
            FormActions(
                HTML( u"""<div class="modal-footer">
                            <input type="submit" name="save" value="Готово" class="btn btn-primary">
                            <a role="button" class="btn btn-default" data-dismiss="modal">Отмена</a>
                     </div>"""),             
        )) 

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer        
        fields = ['date_departure', 'time_departure', 'place_departure', 'place_arrival',
                  'quantity_total', 'quantity_adult', 'quantity_member']    
        widgets = {                       
            'date_departure'  : forms.TextInput( attrs={'class': 'input-sm' , 'id': 'trans_date_departure'}),
            'time_departure'  : forms.TextInput( attrs={'class': 'input-sm' , 'id': 'trans_time_departure'}),
            'place_departure' : forms.Select( attrs={'class': 'input-sm' , 'id': 'trans_place_departure'}),
            'place_arrival'   : forms.Select( attrs={'class': 'input-sm' , 'id': 'trans_place_arrival'}),            
            'quantity_total'  : forms.NumberInput( attrs={'class': 'input-sm' , 'id': 'trans_quantity_total'}),
            'quantity_adult'  : forms.NumberInput( attrs={'class': 'input-sm' , 'id': 'trans_quantity_adult'}),
            'quantity_member' : forms.NumberInput( attrs={'class': 'input-sm' , 'id': 'trans_quantity_member'}), 
        }
        error_messages = {
            'date_departure':   {'required': _(u"Укажите дату отбытия!"), },
            'time_departure':   {'required': _(u"Укажите время отбытия!"), },
            'place_departure':  {'required': _(u"Введите адрес места отбытия!"), },
            'place_arrival':    {'required': _(u"Введите адрес места прибытия!"), },
            'quantity_total':   {'required': _(u"Укажите общее количество!"), },
            'quantity_adult':   {'required': _(u"Укажите количество взрослых!"), }, 
            'quantity_member':  {'required': _(u"Укажите количество участников!"), },        
        }
    def __init__(self, *args, **kwargs):        
        # фильтрация в place_departure
        _user = kwargs.pop('_user', None)   # в этом параметре берем юзер_ид (директора) для фильтрации в subgroup
               
        super(TransferForm, self).__init__(*args, **kwargs)
        
        _choices = [
            ('', '--------'), ('-1', u'Санаторий «Мечта»'),
            ('-2', u'Санаторий «Жемчужина Чувашии»'), ('-3', u'Набережная г. Чебоксары')
            ] + list(Place_departure_choices.objects.filter(user_id = _user).values_list('id', 'place_name'))
        self.fields['place_departure'].choices = _choices
        self.fields['place_arrival'].choices = _choices

        self.helper = FormHelper(self)
        self.helper.form_id = 'id-TransferForm'
        self.helper.form_class = 'form-horizontal'        
        self.helper.label_class = 'col-xs-2'
        self.helper.field_class = 'col-xs-8'        
        self.helper.layout.append(
            FormActions(
                HTML( u"""<div class="modal-footer">
                            <input type="submit" name="save" value="Готово" class="btn btn-primary">
                            <a role="button" class="btn btn-default" data-dismiss="modal">Отмена</a>
                     </div>"""),                
        )) 
    
    def clean(self):
        cleaned_data = super(TransferForm, self).clean()         
        _count_ALL    = cleaned_data.get('quantity_total') if cleaned_data.get('quantity_total') else 0
        _count_adult  = cleaned_data.get('quantity_adult') if cleaned_data.get('quantity_adult') else 0
        _count_member = cleaned_data.get('quantity_member') if cleaned_data.get('quantity_member') else 0                
        # если не сделать эту проверку , будет ругаться на nontype        
        if (_count_ALL != _count_adult + _count_member):
            print u"Общее количество не совпадает с суммой участников и взрослых"                    
            raise forms.ValidationError(u"Общее количество не совпадает с суммой участников и взрослых")        

class ExcursionForm(forms.ModelForm):
    #tour_form =  forms.Select(attrs={'class': 'input-sm', 'id': 'ex_tour_form'})
    #date_departure = forms.DateField(widget=DateWidget(options = dateOptions,  attrs={'class': 'input-sm', 'id': 'ex_date_departure'}, bootstrap_version=3))
    class Meta:
        model = Excursion
        #exclude = ['user']  
        fields = ['tour_form', 'date_departure', 'time_departure', 'place_departure', 'place_arrival',
                  'quantity_total', 'quantity_adult', 'quantity_member']       
        widgets = {
            'tour_form'       : forms.Select(      attrs={'class': 'input-sm', 'id': 'ex_tour_form'}),
            'date_departure'  : forms.TextInput(   attrs={'class': 'input-sm datetimepicker', 'id': 'ex_date_departure'}),            
            'time_departure'  : forms.TextInput(   attrs={'class': 'input-sm', 'id': 'ex_time_departure'}), 
            'place_departure' : forms.Select(      attrs={'class': 'input-sm', 'id': 'ex_place_departure'} ),
            'place_arrival'   : forms.Select(      attrs={'class': 'input-sm', 'id': 'ex_place_arrival'} ),
            'quantity_total'  : forms.NumberInput( attrs={'class': 'input-sm', 'id': 'ex_quantity_total'} ),
            'quantity_adult'  : forms.NumberInput( attrs={'class': 'input-sm', 'id': 'ex_quantity_adult'} ),
            'quantity_member': forms.NumberInput(  attrs={'class': 'input-sm', 'id': 'ex_quantity_member'} ),
        }     
        error_messages = {
            'tour_form':        {'required': _(u"Выберите форму экскурсии!"), },
            'date_departure':   {'required': _(u"Укажите дату отбытия!"), },
            'time_departure':   {'required': _(u"Укажите время отбытия!"), },
            'place_departure':  {'required': _(u"Введите адрес места отбытия!"), },
            'place_arrival':    {'required': _(u"Введите адрес места прибытия!"), },
            'quantity_total':   {'required': _(u"Укажите общее количество!"), },
            'quantity_adult':   {'required': _(u"Укажите количество взрослых!"), }, 
            'quantity_member':  {'required': _(u"Укажите количество участников!"), },        
        }   
    def __init__(self, *args, **kwargs):
        _user = kwargs.pop('_user', None)   # в этом параметре берем юзер_ид (директора) для фильтрации в subgroup
        
        super(ExcursionForm, self).__init__(*args, **kwargs)

        _choices = [
            ('', '--------'), ('-1', u'Санаторий «Мечта»'),
            ('-2', u'Санаторий «Жемчужина Чувашии»'), ('-3', u'Набережная г. Чебоксары')
            ] + list(Place_departure_choices.objects.filter(user_id = _user).values_list('id', 'place_name'))
        self.fields['place_departure'].choices = _choices
        self.fields['place_arrival'].choices = _choices
        
        
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-ExcursionForm'
        self.helper.form_class = 'form-horizontal'        
        self.helper.label_class = 'col-xs-2'
        self.helper.field_class = 'col-xs-8'        
        self.helper.layout.append(
            FormActions(
                HTML( u"""<div class="modal-footer">
                            <input type="submit" name="save" value="Готово" class="btn btn-primary">
                            <a role="button" class="btn btn-default" data-dismiss="modal">Отмена</a>
                     </div>"""),                      
                #Submit('save', 'Submit'),
        )) 

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food      
        fields = ['place_of_residing' , 'date', 'quantity_adult', 'quantity_member',]
                  #'zavtrak', 'obed', 'ugin', ]
        widgets = {
            'place_of_residing' : forms.Select(      attrs={'class': 'input-sm' , 
                                                            'id': 'food_place_of_residing'}),
            'date'   : forms.TextInput( attrs={'class': 'input-sm', 'id': 'food_date'}),
            'quantity_total'    : forms.NumberInput( attrs={'class': 'input-sm' , 
                                                            'id': 'food_quantity_total'}),
            'quantity_adult'    : forms.NumberInput( attrs={'class': 'input-sm', 'id': 'food_quantity_adult'}),
            'quantity_member'   : forms.NumberInput( attrs={'class': 'input-sm', 'id': 'food_quantity_member'}),
            'zavtrak_adult'     : forms.CheckboxInput( attrs={'class': 'input-sm', 'id': 'food_zavtrak_adult'}),
            'obed_adult'        : forms.CheckboxInput( attrs={'class': 'input-sm', 'id': 'food_obed_adult'}),
            'ugin_adult'        : forms.CheckboxInput( attrs={'class': 'input-sm', 'id': 'food_ugin_adult'}),             
        }
        error_messages = {
            'place_of_residing':    {'required': _(u"Выберите место проживания!"), },
            'date'          :       {'required': _(u"Укажите дату заезда!"), },
            #'quantity_total':       {'required': _(u"Укажите общее количество проживающих!"), },
            'quantity_adult':       {'required': _(u"Укажите количество взрослых!"), },            
            'quantity_member':      {'required': _(u"Укажите количество участников!"), },            
                                 
        }
    def __init__(self, *args, **kwargs):
        _user = kwargs.pop('_user', None)   # в этом параметре берем юзер_ид (директора) для фильтрации ПОКА не используется ,но сделал по аналогии с экскурсиями и трансферами
        super(FoodForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-FoodForm'
        self.helper.form_class = 'form-horizontal'        
        self.helper.label_class = 'col-xs-2'
        self.helper.field_class = 'col-xs-8'        
        self.helper.layout.append(
            FormActions(
                HTML(u"""<div class="form-group">
                        <div class="controls col-xs-offset-2 col-xs-8"> 
                            <div class="checkbox input-sm" id="div_id_group">
                                <label class="" for="food_zavtrak"> 
                                    <input type="checkbox" name="zavtrak" id="food_zavtrak" class="checkboxinput"/>
                                    Завтрак
                                </label>
                                
                                <label for="food_obed" class=""> 
                                    <input class="checkboxinput" id="food_obed" name="obed" type="checkbox"/>
                                        Обед
                                </label> 

                                <label for="foog_ugin" class=""> 
                                    <input class="checkboxinput" id="food_ugin" name="ugin" type="checkbox"/>
                                        Ужин
                                </label> 
                            </div> 
                        </div> 
                    </div> 
                
                 <div class="modal-footer">
                            <input type="submit" name="save" value="Готово" class="btn btn-primary">
                            <a role="button" class="btn btn-default" data-dismiss="modal">Отмена</a>
                </div>"""),             
        )) 