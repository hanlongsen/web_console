# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.http import JsonResponse

from ssh.models import Host,HostGroup
from ssh.command import Shell 
from common.utils import get_body,set_response,jresp



class vim(View):
	def get(self,request,*args,**kwargs):
		pass

class HostView(View):
	def get(self,request,*args,**kwargs):
		host_group_id = request.GET.get("host_group_id")
		if not host_group_id:
			hosts = Host.objects.get_values()
		else:
			hosts = Host.objects.get_values(group=int(host_group_id))
		for host in hosts:
			group_name = HostGroup.objects.get(id=host.get("group_id")).group_name
			host["group_name"] = group_name
		return jresp(set_response("200","host query successd",hosts))
	def post(self,request,*args,**kwargs):
		ok,body = get_body(request)
		if not ok:
			return jresp(body)
		host_group_id = body.get("host_group_id")
		host_list = body.get("host_list")
		try:
			host_group = HostGroup.objects.get(id=host_group_id)
		except Exception as e:
			return jresp(set_response("500","host group not found"))
		hosts = Host.objects.filter(group=host_group_id)
		for host in host_list:
			try:
				hosts.get(host_ip=host.get("host_ip"))
				continue
			except Exception as e:
				Host.objects.create(host_ip=host.get("host_ip"),host_port=host.get("host_port"),group=host_group)
		return jresp(set_response("200","host create successd",host_list))
	def delete(self,request,*args,**kwargs):
		host_id = request.GET.get("host_id")
		if not host_id:
			return jresp(set_response("400","host_group_id and host_id must be define"))
		try:
			host = Host.objects.get(id=host_id)
		except Exception as e:
			return jresp(set_response("400","host not found"))
		host.delete()
		return jresp(set_response("200","delete successd"))

	def options(self,request,*args,**kwargs):
		return jresp(set_response("200","delete successd"))

	
	# def delete(self,request,*args,**kwargs):
	# 	host_group_id = request.GET.get("host_group_id")
	# 	host_id = request.GET.get("host_id")
	# 	if not host_group_id or not host_id:
	# 		return jresp(set_response("400","host_group_id and host_id must be define"))
	# 	host_del = [host for host in Host.objects.get_values(group=int(host_group_id)) if host.get("id")==host_id]
	# 	if not host_del:
	# 		return jresp(set_response("400","host not in hostgroup"))
	# 	if len(host_del)>1:
	# 		return jresp(set_response("400","host is repeat"))
	# 	host_del[0].delete()
	# 	return jresp(set_response("200","delete successd"))

class HostGroupView(View):
	def get(self,request,*args,**kwargs):
		host_group_list = HostGroup.objects.get_values()
		return jresp(set_response("200","host query successd",host_group_list))

	def post(self,request,*args,**kwargs):
		ok,body = get_body(request)
		if not ok:
			return jresp(body)
		group_name = body.get("group_name")
		user_name = body.get("user_name")
		passwd = body.get("passwd")
		if not group_name or not user_name or not passwd:
			return jresp(set_response("500","主机名、用户、密码不能为空"))
		try:
			HostGroup.objects.get(group_name=group_name)
			return jresp(set_response("500","host group is exist"))
		except Exception as e:
			pass
		host_group = HostGroup.objects.create(group_name=group_name,user_name=user_name,passwd=passwd)
		return jresp(set_response("200","host group create successd",host_group.group_name))
	def delete(self,request,*args,**kwargs):
		group_id=request.GET.get("group_id")
		if not group_id:
			return jresp(set_response("500","group not found"))
		hostgroup=HostGroup.objects.get(id=group_id)
		host=hostgroup.host_set.all()
		if host.count()!=0:
			return jresp(set_response("500","group is not empty,cant be remove"))
		hostgroup.delete()
		return jresp(set_response("200","group remove success",group_id))
	
	def options(self,request,*args,**kwargs):
		return jresp(set_response("200","delete successd"))
		
class ShellView(View):
	def post(self,request,*args,**kwargs):
		ok,body = get_body(request)
		if not ok:
			return jresp(body)
		cmd = body.get("cmd")
		host_list = body.get("host_list")
		if not cmd:
			return jresp(set_response("500","cmd not found","cmd not found"))
		if len(host_list)==0:
			return jresp(set_response("500","host_list is empty","host_list is empty"))
		print(host_list)
		user="haqiaolong"
		passwd='123456'
		c = Shell(user,passwd,host_list)
		result = c.exe(cmd)
		print(result)
		return jresp(set_response("200","shell exec successd",result))
			
	
class VimView(View):
	def get(self,request,*args,**kwargs):
		pass
		
