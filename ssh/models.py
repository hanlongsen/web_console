# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class ModelMng(models.Manager):
	def get_values(self,**filter):
		print(filter)
		qsets = self.filter(**filter).values()
		if len(filter.keys())==0:
			qsets = self.all().values()
		values = [qset for qset in qsets ]
		return values

class HostGroup(models.Model):
	group_name = models.CharField(max_length=100)
	user_name = models.CharField(max_length=100)
	passwd = models.CharField(max_length=100)
	objects = ModelMng()

class Host(models.Model):
	group = models.ForeignKey(HostGroup)
	host_ip = models.CharField(max_length=100)
	host_port = models.CharField(max_length=10)
	objects = ModelMng()


