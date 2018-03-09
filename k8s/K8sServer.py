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
			poddict["status"]=pod.status.phase
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
			eventdict["messate"]=event.message
			eventdict["namespace"]=event.metadata.namespace
			eventdict["involved_kind"]=event.involved_object.kind
			eventdict["involved_name"]=event.involved_object.name
			eventlist.append(eventdict)
		return eventlist
	def getall(self,**filter):

		events=Event().getall()
		return self.format(events.items)

	def getforns(self,ns,**filter):
		events=Event().getforns(ns)
		return self.format(events.items)

	def getforkind(self,ns,kind,kind_name):
		events=self.getforns(ns)
		myevent=None
		for event in events:
			if kind in event and name in event:
				myevent=event
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