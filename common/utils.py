#coding:utf8
import json
from django.http import JsonResponse
def set_response(status,message,data=[]):
	return dict(status=status,message=message,data=data)

def get_body(request):
	try:
	    body = json.loads(request.body)
	    return 1,body
	except Exception as e:
	    body = set_response("500","解析错误")
	    return 0,body

def jresp(res):
	jr = JsonResponse(res)
	jr["Access-Control-Allow-Origin"] = "http://10.112.184.2:9991"
	jr["Access-Control-Allow-Methods"] ="PUT,DELETE,GET,POST,OPTIONS"
	jr['Access-Control-Allow-Headers'] = 'X-HTTP-Method-Override,cache-control,content-type,hash-referer,x-requested-with'
	return jr

class Result(object):
	@staticmethod
	def error(message):
		return jresp(set_response("500",message))

	@staticmethod
	def ok(message,data=[]):
		return jresp(set_response("200",message,data))

