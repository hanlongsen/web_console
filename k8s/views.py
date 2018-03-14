# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from common.utils import get_body,Result,jresp,set_response
from django.http import HttpResponse
from django.http import JsonResponse


from k8s.K8sServer import GetNamespace,GetEvent,RsFactory

# Create your views here.
class K8sNs(View):
	def get(self,request,*args,**kwargs):
		return Result.ok("ok",GetNamespace().getall())



class K8sResource(View):
	def get(self,request,*args,**kwargs):
		kind=request.GET.get("kind")
		namespace=request.GET.get("namespace") or "all"
		name=request.GET.get("name") or None
		result=""
		if not kind:
			return Result.error("kind is not define")
		if namespace=="all":
			result=RsFactory(kind).getall()
		elif name==None and namespace!="all":
			result=RsFactory(kind).getforns(namespace)
		elif namespace!="all" and name!=None:
			result=RsFactory(kind).getforname(namespace,name)
		return Result.ok("ok",result)

	def options(self,request,*args,**kwargs):
		return Result.ok('ok')


class K8sEvent(View):
	def get(self,request,*args,**kwargs):
		namespace=request.GET.get("namespace")
		kind=request.GET.get("kind")
		name=request.GET.get("name")
		result=GetEvent().getforkind(namespace,kind,name)
		return Result.ok("ok",result)


class test(View):
	def get(self,request,*args,**kwargs):
		return Result.ok("ok",RsFactory("pod").getforns("kube-system"))
