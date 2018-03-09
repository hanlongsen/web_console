from django.conf.urls import url
from django.contrib import admin

from k8s import views

urlpatterns = [
	url(r'^k8sns/$', views.K8sNs.as_view()),
	url(r'^k8sresource/$', views.K8sResource.as_view()),
	url(r'^k8sevent/$', views.K8sEvent.as_view()),
]
