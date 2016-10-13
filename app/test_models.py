# -*- coding: utf-8 -*-


import django
from django.test import TestCase

from django.core.urlresolvers import reverse #django.urls import reverse # waiting to 1.10.

from datetime import datetime
from app.models import Album, Foto, Video


class TestModels(TestCase):
    """  Video models """

    def setUp(self):
        self.album = Album.objects.create(title='test_title', order_num = 1)
    
    def test_foto_returned_str(self):
        _foto = Foto(title='test_foto', album = self.album)
        self.assertEquals(
            str(_foto),
            'test_foto',
        )

    def test_video_returned_str(self):
        _video = Video(title='test_video', album = self.album)
        self.assertEquals(
            str(_video),
            'test_video',
        )
        