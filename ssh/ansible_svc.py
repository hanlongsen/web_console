from ansible import constants as C
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase


# Creat a callback object so we can capture the output
class ResultsCollector(CallbackBase):

	def __init__(self, *args, **kwargs):
	    super(ResultsCollector, self).__init__(*args, **kwargs)
	    self.host_ok     = {}
	    self.host_unreachable = {}
	    self.host_failed = {}
	
	def v2_runner_on_unreachable(self, result):
	    self.host_unreachable[result._host.get_name()] = result
	
	def v2_runner_on_ok(self, result,  *args, **kwargs):
	    self.host_ok[result._host.get_name()] = result
	
	def v2_runner_on_failed(self, result,  *args, **kwargs):
	    self.host_failed[result._host.get_name()] = result


def run(host,user,passwd,tasks):
	Options = namedtuple('Options', ['connection','module_path', 'forks','remote_user',
	        'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
	        'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])
	
	# initialize needed objects
	variable_manager = VariableManager()
	loader = DataLoader()
	options = Options(connection='smart', module_path='none', forks=100,remote_user=user,
	   		private_key_file=None, ssh_common_args=None, ssh_extra_args=None,
	        sftp_extra_args=None, scp_extra_args=None, become=True, become_method="sudo",
	        become_user="root", verbosity=None, check=False)
	passwords = { 'conn_pass': passwd , 'become_pass': "" }
	inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=host)
	variable_manager.set_inventory(inventory)
	host_list=[]
	for h in host:
		host_list.append(h.split(":")[0])
	play_source =  dict(
	        name = "Ansible Play",
	        hosts = host_list,
	        gather_facts = 'no',
	        tasks = tasks 
	    )
	print(play_source)
	play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
	
	tqm = None
	callback = ResultsCollector()
	try:
		tqm = TaskQueueManager(
		        inventory=inventory,
		        variable_manager=variable_manager,
		        loader=loader,
		        options=options,
		        passwords=passwords,
		    )
		tqm._stdout_callback = callback
		tqm.run(play)
	finally:
		if tqm is not None:
			tqm.cleanup()
	return callback.host_ok.items(),callback.host_failed.items(),callback.host_unreachable.items()

	

class PlayTask(object):
	support_tasks = ['file','shell','service']
	def action(self,module,args):
	    return dict(action=dict(module=module, args=args)) 
	def fetch(self,src,dest):
	    return self.action('fetch',dict(src=src,dest=dest))
	def shell(self,cmd):
	    return self.action('shell',cmd)
	def service(self,svc):
	    return self.action('service',dict(name=svc,state='reloaded'))
	def file(self,path,mode):
		return self.action('file',dict(path=path,mode=mode))
	def copy(self,src,dest):
		return self.action('copy',dict(src=src,dest=dest))



if __name__ == '__main__':
	host_list = ["10.114.249.6:22","10.114.249.16:22"]
	user="haqiaolong"
	passwd='123456'
	tasks=[]
	task1=PlayTask().shell('df -h')
	task2=PlayTask().fetch('/etc/kubernetes/kubelet','/home/')
	task3=PlayTask().file('/root/docker-enter','0755')
	tasks.append(task1)
	success,fail,unreachable = run(host_list,user,passwd,tasks)
	
	print "UP ***********"
	for host, result in success:
		print '{0}\n{1}'.format(host, result._result.get('stdout'))
	
	print "FAILED *******"
	for host, result in fail:
		print '{0} >>> {1}'.format(host, result._result['msg'])
	
	print "DOWN *********"
	for host, result in unreachable:
		print '{0} >>> {1}'.format(host, result._result['msg'])


