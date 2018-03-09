from kubernetes import client, config
config.load_kube_config("/var/lib/kubelet/kubeconfig")

class Base(object):
	def __init__(self):
		self.v1=client.CoreV1Api()
		self.appsv1=client.AppsV1beta1Api()

class Namespace(Base):
	def getall(self,**filter):
		return self.v1.list_namespace(**filter)

class Pod(Base):
	def getall(self,**filter):
		return self.v1.list_pod_for_all_namespaces(**filter)
	def getforns(self,ns,**filter):
		return self.v1.list_namespaced_pod(ns,**filter)


class Deployment(Base):
	def getall(self,**filter):
		return self.appsv1.list_deployment_for_all_namespaces(**filter)

	def getforns(self,ns,**filter):
		return self.appsv1.list_namespaced_deployment(ns,**filter)


class Replicaset(Base):
	def getall(self,**filter):
		return self.appsv1.list_replica_set_for_all_namespaces(**filter)
	def getforns(self,ns,**filter):
		return self.AppsV1beta1Api.list_namespaced_replica_set(ns,**filter)


class Event(Base):
	def getall(self,**filter):
		return self.v1.list_event_for_all_namespaces(**filter)
	def getforns(self,ns,**filter):
		return self.v1.list_namespaced_event(ns,**filter)