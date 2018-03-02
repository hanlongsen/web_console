from django.conf.urls import url
from django.contrib import admin
from ssh import views


urlpatterns = [
	url(r'^hostgroup/$', views.HostGroupView.as_view()),
	url(r'^host/$', views.HostView.as_view()),
	url(r'^shell/$', views.ShellView.as_view()),
]
