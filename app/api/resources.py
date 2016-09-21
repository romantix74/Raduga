# -*- coding: utf-8 -*-
from tastypie.resources import ModelResource
from tastypie import fields
from app.models import Album, Foto, Director

from tastypie.authentication import BasicAuthentication, SessionAuthentication
from tastypie.authorization import DjangoAuthorization, Authorization

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

class DirectorResource(ModelResource):
    class Meta:
        queryset = Director.objects.all()
        resource_name = 'director'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        allowed_methods = ['get', 'post']
        authentication =  SessionAuthentication() #BasicAuthentication()  #
        authorization = Authorization()
    
    #функции ограничивающие действия , только для объекта-Director , под которым мы залогинились
    def obj_create(self, bundle, **kwargs):
        return super(DirectorResource, self).obj_create(bundle, user=bundle.request.user)

    def authorized_read_list(self, object_list, bundle):        
        return object_list.filter(user=bundle.request.user)