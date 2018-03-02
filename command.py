from ssh.ansible_svc import run,PlayTask
class abase(object):
	def __init__(self,user,passwd,host_list):
		self.user=user
		self.passwd=passwd
		self.host_list=host_list
	def get_result(self,success,fail,unreachable):

		result_success_list=[]
		result_fail_list=[]
		result_unreachable_list=[]
		for host, result in success:
			result_ok_dict = {}
			result_ok_dict["host"] = host
			result_ok_dict["result"] = result._result.get('stdout')
			result_ok_list.append(result_ok_dict)
		for host, result in fail:
            result_fail_dict = {}
            result_fail_dict["host"] = host
            result_fail_dict["result"] = result._result['msg']
            result_fail_list.append(result_fail_dict)
		for host, result in unreachable:
			result_unreachable_dict = {}
			result_unreachable_dict["host"] = host
			result_unreachable_dict["result"] = result._result['msg']
			result_unreachable_list.append(result_fail_dict)
		
class shell(abase):
	def exec(self,shell):
		task=[]
		task=PlayTask().shell(shell)
		tasks.append(task)
		return self.get_result(run(self.host_list,self.user,self.passwd,tasks))	
