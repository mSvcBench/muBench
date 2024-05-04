import json
import os
import yaml
from pprint import pprint


K8s_YAML_BUILDER_PATH = os.path.dirname(os.path.abspath(__file__))

SIDECAR_TEMPLATE = "- name: %s-sidecar\n          image: %s"
NODE_AFFINITY_TEMPLATE = {'affinity': {'nodeAffinity': {'requiredDuringSchedulingIgnoredDuringExecution': {'nodeSelectorTerms': [{'matchExpressions': [{'key': 'kubernetes.io/hostname','operator': 'In','values': ['']}]}]}}}}
POD_ANTIAFFINITI_TEMPLATE = {'affinity':{'podAntiAffinity':{'requiredDuringSchedulingIgnoredDuringExecution':[{'labelSelector':{'matchExpressions':[{'key':'app','operator':'In','values':['']}]},'topologyKey':'kubernetes.io/hostname'}]}}}

# Override work_model params with those in k8s_parameters
def customization_work_model(model, k8s_parameters):
    for service in model:
        model[service].update({"url": f"{service}.{k8s_parameters['namespace']}.svc.{k8s_parameters['cluster_domain']}.local"})
        model[service].update({"path": k8s_parameters['path']})
        model[service].update({"image": k8s_parameters['image']})
        model[service].update({"namespace": k8s_parameters['namespace']})
                    
        if "scheduler-name" in model[service].keys():
            # override scheduler-name value of workmodel.json
            model[service].update({"scheduler-name": k8s_parameters['scheduler-name']})
        if "replicas" in k8s_parameters.keys():
            # override replica value of workmodel.json
            model[service].update({"replicas": k8s_parameters['replicas']})
        if "cpu-requests" in k8s_parameters.keys():
            # override cpu-requests value of workmodel.json
            model[service].update({"cpu-requests": k8s_parameters['cpu-requests']})
        if "cpu-limits" in k8s_parameters.keys():
            # override cpu-limits value of workmodel.json
            model[service].update({"cpu-limits": k8s_parameters['cpu-limits']})
        if "memory-requests" in k8s_parameters.keys():
            # override memory-requests value of workmodel.json
            model[service].update({"memory-requests": k8s_parameters['memory-requests']})
        if "memory-limits" in k8s_parameters.keys():
            # override memory-limits value of workmodel.json
            model[service].update({"memory-limits": k8s_parameters['memory-limits']})
    print("Work Model Updated!")


def create_deployment_yaml_files(model, k8s_parameters, nfs, output_path):
    namespace = k8s_parameters['namespace']
    counter=0
    for service in model:
        counter=counter+1
        with open(f"{K8s_YAML_BUILDER_PATH}/Templates/DeploymentTemplate.yaml", "r") as file:
            f = file.read()
            f = f.replace("{{SERVICE_NAME}}", service)
            f = f.replace("{{IMAGE}}", model[service]["image"])
            f = f.replace("{{NAMESPACE}}", namespace)
            if "scheduler-name" in model[service].keys():
                f = f.replace("{{SCHEDULER_NAME}}", str(model[service]["scheduler-name"]))
            else:
                f = f.replace("{{SCHEDULER_NAME}}", "default-scheduler")
            if "sidecar" in model[service].keys():
                f = f.replace("{{SIDECAR}}", SIDECAR_TEMPLATE % (service, model[service]["sidecar"]))
            else:
                f = f.replace("{{SIDECAR}}", "".rstrip())
            if "replicas" in model[service].keys():
                f = f.replace("{{REPLICAS}}", str(model[service]["replicas"]))
            else:
                f = f.replace("{{REPLICAS}}", "1")
            if "node_affinity" in model[service].keys():
                NODE_AFFINITY_TEMPLATE_TO_ADD = NODE_AFFINITY_TEMPLATE
                NODE_AFFINITY_TEMPLATE_TO_ADD['affinity']['nodeAffinity']['requiredDuringSchedulingIgnoredDuringExecution']['nodeSelectorTerms'][0]['matchExpressions'][0].update({"values" : model[service]["node_affinity"]})
                f = f.replace("{{NODE_AFFINITY}}", str(yaml.dump(NODE_AFFINITY_TEMPLATE_TO_ADD)).rstrip().replace('\n','\n   '))
            else:
                f = f.replace("{{NODE_AFFINITY}}", "")
            if "pod_antiaffinity" in model[service].keys() and model[service]['pod_antiaffinity']==True:
                POD_ANTIAFFINITY_TO_ADD = POD_ANTIAFFINITI_TEMPLATE
                POD_ANTIAFFINITY_TO_ADD['affinity']['podAntiAffinity']['requiredDuringSchedulingIgnoredDuringExecution'][0]['labelSelector']['matchExpressions'][0]['values'][0] = service
                POD_ANTIAFFINITY_TO_ADD = str(yaml.dump(POD_ANTIAFFINITY_TO_ADD)).replace('\n','\n        ').rstrip()
                f = f.replace("{{POD_ANTIAFFINITY}}", POD_ANTIAFFINITY_TO_ADD)
            else:
                f = f.replace("{{POD_ANTIAFFINITY}}", "".rstrip())
            if "workers" in model[service].keys():
                f = f.replace("{{PN}}", f'\'{model[service]["workers"]}\'')
            else:
                f = f.replace("{{PN}}", "\'1\'") 
            if "threads" in model[service].keys():
                f = f.replace("{{TN}}", f'\'{model[service]["threads"]}\'')
            else:
                f = f.replace("{{TN}}", "\'4\'")
            
            rank_string='' # ranck string is used to order the yaml file as a funciont of the cpu-requests 
            if  len(set(model[service].keys()).intersection({"cpu-limits","memory-limits","cpu-requests","memory-requests"})):
                s=""
                if "cpu-requests" in model[service].keys() or "memory-requests" in model[service].keys():
                    s = s + "\n            requests:"
                    if "cpu-requests" in model[service].keys():
                        s = s + "\n              cpu: " + model[service]["cpu-requests"]
                        if 'm' in model[service]["cpu-requests"]:
                            rank_string=str(int(model[service]["cpu-requests"].replace('m',''))).zfill(5)
                        else:
                            rank_string=str(int(float(model[service]["cpu-requests"])*1000)).zfill(5)
                    if "memory-requests" in model[service].keys():
                        s = s + "\n              memory: " + model[service]["memory-requests"]
                if "cpu-limits" in model[service].keys() or "memory-limits" in model[service].keys():
                    s = s + "\n            limits:"
                    if "cpu-limits" in model[service].keys():
                        s = s + "\n              cpu: " + model[service]["cpu-limits"]
                    if "memory-limits" in model[service].keys():
                        s = s + "\n              memory: " + model[service]["memory-limits"]
                f = f.replace("{{RESOURCES}}", s)
            else:
                f= f.replace("{{RESOURCES}}", "{}")
        if not os.path.exists(f"{output_path}/yamls"):
            os.makedirs(f"{output_path}/yamls")
        
        # rank used to sort the deployment so as more demanding PODs are deployed first
        with open(f"{output_path}/yamls/{str(rank_string).zfill(3)}-{k8s_parameters['prefix_yaml_file']}-{service}.yaml", "w") as file:
            file.write(f)

    with open(f"{K8s_YAML_BUILDER_PATH}/Templates/ConfigMapNginxGwTemplate.yaml", "r") as file:
        f = file.read()
        f = f.replace("{{NAMESPACE}}", namespace)
        f = f.replace("{{PATH}}", k8s_parameters["path"])
        f = f.replace("{{RESOLVER}}", k8s_parameters["dns-resolver"])

    with open(f"{output_path}/yamls/ConfigMapNginxGw.yaml", "w") as file:
        file.write(f)

    with open(f"{K8s_YAML_BUILDER_PATH}/Templates/DeploymentNginxGwTemplate.yaml", "r") as file:
        f = file.read()
        f = f.replace("{{NAMESPACE}}", namespace)
        if "scheduler-name" in model[service].keys():
            f = f.replace("{{SCHEDULER_NAME}}", str(model[service]["scheduler-name"]))
        else:
            f = f.replace("{{SCHEDULER_NAME}}", "default-scheduler")

    with open(f"{output_path}/yamls/DeploymentNginxGw.yaml", "w") as file:
        file.write(f)

    print("Deployment Created!")
