from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin
from app.models import Album, Foto, Video

class EntryResourceTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super(EntryResourceTest, self).setUp()

        self.album1 = Album(title = 'test_title_1', order_num = 1)
        self.album1.save()
        self.album2 = Album(title = 'test_title_2', order_num = 1)
        self.album2.save()
        
        self.foto1 = Foto(album = self.album1, title='foto1', image='test_image_1.jpg')
        self.foto2 = Foto(album = self.album1, title='foto2', image='test_image_2.jpg')

        self.video1 = Video(album = self.album2, title='video1', video_link='test_video_link2')
        self.video2 = Video(album = self.album2, title='video2', video_link='test_video_link2')

    def test_get_albums(self):
        resp = self.api_client.get('/api/v1/album/', format='json')
        self.assertValidJSONResponse(resp)
        self.assertEqual(len(self.deserialize(resp)['objects']), 2)
        self.assertEqual(self.deserialize(resp)['objects'][0], {
            u'id': self.album1.pk,
            u'title': u'{0}'.format(self.album1.title),  
            u'image': None,           
            u'order_num': self.album1.order_num,
            u'resource_uri': u'/api/v1/album/{0}/'.format(self.album1.pk)
        })
    
    def test_get_foto_from_album_1(self):
        resp = self.api_client.get('/api/v1/foto/?album_id__id=' + str(self.album1.id), format='json')
        self.assertValidJSONResponse(resp)
        self.assertEqual(len(self.deserialize(resp)), 2)
        #self.assertEqual(self.deserialize(resp)['objects'][0], {
        #    u'id': self.album1.pk,
        #    u'title': u'{0}'.format(self.album1.title),  
        #    u'image': None,           
        #    u'order_num': self.album1.order_num,
        #    u'resource_uri': u'/api/v1/album/{0}/'.format(self.album1.pk)
        #})

    def test_get_VIDEO_from_album_1(self):
        resp = self.api_client.get('/api/v1/video/?album_id__id=' + str(self.album1.id), format='json')
        self.assertValidJSONResponse(resp)
        self.assertEqual(len(self.deserialize(resp)), 2)