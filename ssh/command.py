from ssh.ansible_svc import run,PlayTask
class Cbase(object):
	def __init__(self,user,passwd,host_list):
		self.user=user
		self.passwd=passwd
		self.host_list=host_list
	def get_result(self,success,fail,unreachable):
		result = {}
		result_success_list=[]
		result_fail_list=[]
		result_unreachable_list=[]
		for host, result in success:
			result_success_dict = {}
			result_success_dict["host"] = host
			result_success_dict["result"] = result._result.get('stdout').encode("utf-8").replace("\n","<br>")
			result_success_list.append(result_success_dict)
		for host, result in fail:
			result_fail_dict = {}
			result_fail_dict["host"] = host
			print(result._result)
			result_fail_dict["result"] = result._result['stderr'].encode("utf-8").replace("\n","<br>")
			result_fail_list.append(result_fail_dict)
		for host, result in unreachable:
			result_unreachable_dict = {}
			result_unreachable_dict["host"] = host
			print(result._result)
			result_unreachable_dict["result"] = result._result['msg'].encode("utf-8").replace("\n","<br>")
			result_unreachable_list.append(result_unreachable_dict)
		result = {"result_success_list":result_success_list,"result_fail_list":result_fail_list,"result_unreachable_list":result_unreachable_list}
		return result
class Shell(Cbase):

	def exe(self,cmd):
		tasks=[]
		task=PlayTask().shell(cmd)
		tasks.append(task)
		success,fail,unreachable = run(self.host_list,self.user,self.passwd,tasks)
		return self.get_result(success,fail,unreachable)	
