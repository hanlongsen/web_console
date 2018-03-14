from k8s.K8sApi import Namespace,Deployment,Replicaset,Event,Pod



class GetNamespace(object):
	def format(self,items):
		nslist=[]
		for ns in items:
			nslist.append(ns.metadata.name)
		return nslist
	def getall(self):

		allns=Namespace().getall()
		return self.format(allns.items)

class GetDeployment(object):
	def format(self,items):
		deploylist=[]
		for deploy in items:
			deploydict={}
			deploydict["name"]=deploy.metadata.name
			deploydict["namespace"]=deploy.metadata.namespace
			deploydict["create_time"]=deploy.metadata.creation_timestamp
			deploydict["current"]=deploy.status.replicas
			deploydict["available"]=deploy.status.available_replicas
			deploydict["updated_replicas"]=deploy.status.updated_replicas
			deploydict["desired"]=deploy.status.replicas
			deploylist.append(deploydict)
		return deploylist

	def getall(self):
		deploys=Deployment().getall()
		return self.format(deploys.items)

	def getforns(self,ns):
		deploys=Deployment().getforns(ns)
		return self.format(deploys.items)

	def getforname(self,ns,name):
		deploys=self.getforns(ns)
		mydeploy=None
		for deploy in deploys:
			if name in deploy.get("name"):
				mydeploy=deploy
		return mydeploy

class GetPod(object):
	def format(self,items):
		podlist=[]
		for pod in items:
			poddict={}
			poddict["name"]=pod.metadata.name
			poddict["namespace"]=pod.metadata.namespace
			poddict["create_time"]=pod.metadata.creation_timestamp
			poddict["pod_ip"]=pod.status.pod_ip
			poddict["host_ip"]=pod.status.host_ip
			mystatus="Running"
			message=""
			restart_counts=0
			for containerstatus in pod.status.container_statuses:
				statusdict={}
				last_running=containerstatus.last_state.running
				last_terminated=containerstatus.last_state.terminated
				last_waiting=containerstatus.last_state.waiting
				running=containerstatus.state.running
				terminated=containerstatus.state.terminated
				waiting=containerstatus.state.waiting
				image=containerstatus.image
				restart_count=containerstatus.restart_count
				restart_counts+=restart_count
				statusdict["image"]=image
				statusdict["restart_count"]=restart_count
				if last_terminated:
					message+="last_terminated_mes:{0},last_terminated_res:{1}".format(last_terminated.message,last_terminated.reason)
					# last_tmmes=dict(message=last_terminated.message,reason=last_terminated.reason)
					# statusdict["last_terminated"]=last_tmmes
				if last_waiting:
					message+="last_waiting_mes:{0},last_waiting_res:{1}".format(last_waiting.message,last_waiting.reason)
					# last_wtmes=dict(message=last_waiting.message,reason=last_waiting.reason)
					# statusdict["last_waiting"]=last_wtmes
				if terminated:
					mystatus=terminated.reason
					message+="terminated_mes:{0},terminated_res:{1}".format(terminated.message,terminated.reason)
					# tmmes=dict(message=terminated.message,reason=terminated.reason)
					# statusdict["terminated"]=tmmes
				if waiting:
					mystatus=waiting.reason
					message+="waiting_mes:{0},waiting_res:{1}".format(waiting.message,waiting.reason)
					# wtmes=dict(message=waiting.message,reason=waiting.reason)
					# statusdict["waiting"]=wtmes
			poddict["restart_count"]=restart_counts
			poddict["status"]=mystatus
			poddict["message"]=message
			print(mystatus)
			podlist.append(poddict)
		return podlist

	def getall(self,**filter):
		pods = Pod().getall()
		return self.format(pods.items)
	def getforns(self,ns,**filter):
		pods=Pod().getforns(ns)
		return self.format(pods.items)
	def getforname(self,ns,name):
		pods=self.getforns(ns)
		mypod=None
		for pod in pods:
			if name in pod.get("name"):
				mypod=pod
		return mypod
class GetEvent(object):
	def format(self,items):
		eventlist=[]
		for event in items:
			eventdict={}
			eventdict["type"]=event.type
			eventdict["reason"]=event.reason
			eventdict["message"]=event.message
			eventdict["namespace"]=event.metadata.namespace
			eventdict["involved_kind"]=event.involved_object.kind
			eventdict["involved_name"]=event.involved_object.name
			eventdict["create_time"]=event.metadata.creation_timestamp
			eventlist.append(eventdict)
		return eventlist
	def getall(self,**filter):

		events=Event().getall()
		return self.format(events.items)

	def getforns(self,ns,**filter):
		events=Event().getforns(ns)
		return self.format(events.items)

	def getforkind(self,ns,kind,rs_name):
		print(ns,kind,rs_name)
		events=self.getforns(ns)
		myevent=[]
		for event in events:
			print(kind,event.get("involved_kind").lower())
			print(rs_name,event.get("involved_name").lower())
			if kind == event.get("involved_kind").lower() and rs_name == event.get("involved_name").lower():
				myevent.append(event)
		return myevent 


class RsFactory(object):
	def __init__(self,kind):
		self.resource=dict(
			pod=GetPod(),
			deployment=GetDeployment()
			)
		self.kind=kind
	def _build(self):
		return self.resource.get(self.kind)
	def getall(self):
		return self._build().getall()
	def getforns(self,ns):
		return self._build().getforns(ns)
	def getforname(self,ns,name):
		return self._build().getforname(ns,name)