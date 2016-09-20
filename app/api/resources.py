# -*- coding: utf-8 -*-
from tastypie.resources import ModelResource
from tastypie import fields
from app.models import Album, Foto

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

class AlbumResource(ModelResource):
    class Meta:
        queryset = Album.objects.all()
        resource_name = 'album'
        allowed_methods = ['get']
        filtering = {
            'id': ALL,   
        }
class FotoResource(ModelResource):
    #album_id = fields.ToOneField(AlbumResource, 'album', full=True )
    album_id = fields.ForeignKey(AlbumResource, 'album',full=True)
    class Meta:
        queryset = Foto.objects.all()
        fields = ['title', 'album', 'image', 'image_small']
        resource_name = 'foto'
        allowed_methods = ['get']
        include_resource_uri = False
        filtering = {
            'album_id': ALL_WITH_RELATIONS,   
        }
    def dehydrate(self, bundle):
        # добавляем поле с превьюшками , потому что оно не сериализируеться
        bundle.data['image_small'] = bundle.obj.image_small.url
        return bundle
        