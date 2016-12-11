from django.conf.urls import url

from . import views

app_name = "OJ"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^problem/$', views.problemset, name='problemset'),
    url(r'^problem/(?P<id>[0-9]+)/$', views.problem, name='problem'),
    url(r'^problem/(?P<id>[0-9]+)/(?P<contest>[0-9]+)/$', views.problem, name='contestproblem'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^status/$', views.statuslist, name='statuslist'),
    url(r'^status/(?P<id>[0-9]+)/$', views.status, name='status'),
    url(r'^status/user/', views.userProblemStatus, name='userstatus'),
    url(r'^contest/$', views.contestList, name="contestlist"),
    url(r'^contest/sign/$',
        views.contestSign, name="contestsign"),
    url(r'^contest/(?P<id>[0-9]+)/$', views.contest, name="contest")
]
