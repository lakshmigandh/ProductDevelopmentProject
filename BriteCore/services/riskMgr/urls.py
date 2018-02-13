from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^svc/riskentity/?(?P<risktype>\w{0,50})/$', views.RiskMgr.as_view()),
    url(r'^(?P<risktype>\w{0,50})/$', views.index, name='index'),
    url(r'^refreshMetaData$', views.refreshMetaData, name='refreshMetaData'),

]
