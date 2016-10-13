# -*- coding: utf-8 -*-

import django
from django.test import TestCase

from django.core.urlresolvers import reverse

from datetime import datetime
from app.models import Director, Album

from django.contrib.auth.models import User

from tastypie.test import ResourceTestCaseMixin

class MainPageViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('dir', 'lennon@thebeatles.com', 'johnpassword') #Director.objects.create( pk = 1 )
        #self.user.last_login = datetime.now()
        self.user.save()
        self.new_dir = Director()
        self.new_dir.user = self.user      
        self.new_dir.director = u'Иванов И.И.'         
        self.new_dir.save(); 
        self.client.force_login(self.user)

    def test_main_page(self):
        response = self.client.get(reverse('home2'), follow = True)  # после восстановления работы сделать просто home

        self.assertEqual(response.status_code, 200)
        assert self.user.is_authenticated()
        self.assertEqual(response.context['directorOfGroup'], Director.objects.get( user_id = 1 )) # dir22 = id 166

# тест заполнения формы и  редактирования Руководителя
class EditDirTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super(EditDirTest, self).setUp()      
        # Create a user.
        self.username = 'dir'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username, 'daniel@example.com', self.password)
        self.client.login( username=self.username, password=self.password)

    # для аутентификации , взял из примера на сайте http://django-tastypie.readthedocs.io/en/latest/testing.html
    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)

    def test_edit_dir_filling_form(self):
        #response = self.client.get(reverse('editDir'), format='json')
        resp = self.client.get('/api/v1/director/', data={'format': 'json'})
        self.assertEqual(resp.status_code, 200)
        #resp = self.api_client.get('/api/v1/director/', format='json', authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)

        #response = self.api_client.get('/api/v1/director/', format='json', authentication=self.user)
        #self.assertValidJSONResponse(response)
        #self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.context['director'], self.new_dir.director)        

# тест заполнения формы и  редактирования Руководителя
#class EditDirTest(TestCase):
#    def

class VideoViewTests(TestCase):
    """ Video page test"""
    def test_url_adn_date_for_video(self):
        response = self.client.get(reverse('video'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['year'], datetime.now().year)
        self.assertTemplateUsed(response, 'app/video_gallery.html')

class FotoViewTest(TestCase):
    """ Foto gallery page"""
    def test_url_and_etc(self):
        response = self.client.get(reverse('foto'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ФОТО ГАЛЛЕРЕЯ")
        self.assertQuerysetEqual(response.context['albums'], Album.objects.all())

