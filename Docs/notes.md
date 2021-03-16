### ServiceMesh
python RunServiceMeshGen.py
Service Mesh Created!
{'s0': [],
 's1': [{'seq_len': 1, 'services': ['s0']}],
 's2': [{'seq_len': 1, 'services': ['s1']}],
 's3': [{'seq_len': 1, 'services': ['s0']}],
 's4': [{'seq_len': 1, 'services': ['s0']}],
 's5': [{'seq_len': 1, 'services': ['s0']}],
 's6': [{'seq_len': 1, 'services': ['s1']}],
 's7': [{'seq_len': 1, 'services': ['s5']}],
 's8': [{'seq_len': 1, 'services': ['s5']}],
 's9': [{'seq_len': 1, 'services': ['s5']}]}
Save service mesh on file? (y) y

******
### WorkModel

Work Model Created!
{'s0': {'params': {'compute_pi': {'mean_bandwidth': 11,
                                  'range_complexity': [101, 101]}}},
 's1': {'params': {'compute_pi': {'mean_bandwidth': 11,
                                  'range_complexity': [101, 101]}}},
 's2': {'params': {'compute_pi': {'mean_bandwidth': 11,
                                  'range_complexity': [101, 101]}}},
 's3': {'params': {'compute_pi': {'mean_bandwidth': 11,
                                  'range_complexity': [101, 101]}}},
 's4': {'params': {'compute_pi': {'mean_bandwidth': 11,
                                  'range_complexity': [101, 101]}}}}
Save work model on file? (y) y


*******
### Builder

Work Model Updated!
{'s0': {'image': 'lucapetrucci/microservice:latest',
        'namespace': 'default',
        'params': {'compute_pi': {'mean_bandwidth': 11,
                                  'range_complexity': [101, 101]}},
        'path': '/api/v1',
        'url': 'http://s0.default.svc.cluster.local'},
 's1': {'image': 'lucapetrucci/microservice:latest',
        'namespace': 'default',
        'params': {'compute_pi': {'mean_bandwidth': 11,
                                  'range_complexity': [101, 101]}},
        'path': '/api/v1',
        'url': 'http://s1.default.svc.cluster.local'},
 's2': {'image': 'lucapetrucci/microservice:latest',
        'namespace': 'default',
        'params': {'compute_pi': {'mean_bandwidth': 11,
                                  'range_complexity': [101, 101]}},
        'path': '/api/v1',
        'url': 'http://s2.default.svc.cluster.local'},
 's3': {'image': 'lucapetrucci/microservice:latest',
        'namespace': 'default',
        'params': {'compute_pi': {'mean_bandwidth': 11,
                                  'range_complexity': [101, 101]}},
        'path': '/api/v1',
        'url': 'http://s3.default.svc.cluster.local'},
 's4': {'image': 'lucapetrucci/microservice:latest',
        'namespace': 'default',
        'params': {'compute_pi': {'mean_bandwidth': 11,
                                  'range_complexity': [101, 101]}},
        'path': '/api/v1',
        'url': 'http://s4.default.svc.cluster.local'}}
Deployment Created!

******** 
### apply
kubectl apply -f yamls
configmap/ms-gateway-configmap created
deployment.apps/ms-gateway-nginx created
service/ms-gw-nginx-svc created
deployment.apps/s0-dep created
service/s0 created
deployment.apps/s1-dep created
service/s1 created
deployment.apps/s2-dep created
service/s2 created
deployment.apps/s3-dep created
service/s3 created
deployment.apps/s4-dep created
service/s4 created
deployment.apps/s5-dep created
service/s5 created
persistentvolume/nfs-pv-ms created
persistentvolumeclaim/nfs-pvc-ms created

