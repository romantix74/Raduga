from django.conf.urls import patterns, include, url
#from app.views import CreateResidingView , UpdateResidingView
from django.views.generic import TemplateView
import app.views

from app.views import FotoView, VideoView


#urlpatterns = patterns('',
urlpatterns = [
    
    #url(r'^$', app.views.home, name='home'),
    url(r'^uploadFoto/$', app.views.UploadFoto_view, name='uploadFoto'),
    url(r'^editDir/$', app.views.EditDir_view, name='editDir'),  
    url(r'^memberFrame/$', app.views.MemberFrame_view, name='memberFrame'),  
    url(r'^createOrEditMember/(?P<member_id>[0-9]+)/$', app.views.CreateOrEditMember_view, name='createOrEditMember'),    
    url(r'^deleteMember/(?P<member_id>[0-9]+)/$', app.views.DeleteMember_view, name='deleteMember'),   
    
    #Participation
    url(r'^participationFrame/$', app.views.ParticipationFrame_view, name='participationFrame'),
    url(r'^createOrEditParticipation/(?P<participation_id>[0-9]+)/$', app.views.CreateOrEditParticipation_view, name='createOrEditParticipation'),
    url(r'^deleteParticipation/(?P<participation_id>[0-9]+)/$', app.views.DeleteParticipation_view, name='deleteParticipation'),

    #Residing
    #url(r'^createResiding/(?P<user_id>[0-9]+)/$', 'raduga.views.CreateResiding_view', name='createResiding'),
    url(r'^residingFrame/$', app.views.ResidingFrame_view, name='residingFrame'),
    url(r'^createOrEditResiding/(?P<residing_id>[0-9]+)/$', app.views.CreateOrEditResiding_view, name='createOrEditResiding'),
    url(r'^deleteResiding/(?P<residing_id>[0-9]+)/$', app.views.DeleteResiding_view, name='deleteResiding'),
    #url(r'^createResiding/(?P<user_id>[0-9]+)/$', CreateResidingView.as_view(), name='createResiding'),
    #url(r'^updateResiding/(?P<req_id>[0-9]+)/$', UpdateResidingView.as_view(), name='updateResiding'),
    
    #Transfer
    url(r'^transferFrame/$', app.views.TransferFrame_view, name='transferFrame'),
    url(r'^createOrEditTransfer/(?P<transfer_id>[0-9]+)/$', app.views.CreateOrEditTransfer_view, name='createOrEditTransfer'),
    url(r'^deleteTransfer/(?P<transfer_id>[0-9]+)/$', app.views.DeleteTransfer_view, name='deleteTransfer'),
    
    #Excursion
    url(r'^excursionFrame/$', app.views.ExcursionFrame_view, name='excursionFrame'),
    url(r'^createOrEditExcursion/(?P<excursion_id>[0-9]+)/$', app.views.CreateOrEditExcursion_view, name='createOrEditExcursion'),
    url(r'^deleteExcursion/(?P<excursion_id>[0-9]+)/$', app.views.DeleteExcursion_view, name='deleteExcursion'),

    #Food
    url(r'^foodFrame/$', app.views.FoodFrame_view, name='foodFrame'),
    url(r'^createOrEditFood/(?P<food_id>[0-9]+)/$', app.views.CreateOrEditFood_view, name='createOrEditFood'),
    url(r'^deleteFood/(?P<food_id>[0-9]+)/$', app.views.DeleteFood_view, name='deleteFood'),

    # foto gallery
    url(r'^foto/$', FotoView.as_view(), name='foto'),
    #url(r'^foto/$', app.views.foto, name='foto'),    

    # video gallery
    url(r'^video/$', VideoView.as_view(), name='video'),
]